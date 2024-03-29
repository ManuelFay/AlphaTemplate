import numpy as np

from neural_scripts.dataset import TemplateDataset
from alpha_template.interfaces.naive_nn import NaiveNet
from neural_scripts.trainer import Trainer, TrainingArgs

from alpha_template.constants.constants import ROW_COUNT, COLUMN_COUNT

# TODO: Adapt to your game
def detect_full_cols(board):
    board = ((board != 0).sum(axis=0) == 6).squeeze()
    return np.where(board)[0].tolist()


def normalize_policies(boards, policies):
    new_pols = []
    for board, pol in zip(boards, policies):
        pol2 = pol.copy()
        for idx in detect_full_cols(board):
            pol2.insert(idx, 0.)
        new_pols.append(pol2)

    return np.array(new_pols)


data_train = np.load("../data/training_2.npy", allow_pickle=True)
data_test = np.load("../data/training_1.npy", allow_pickle=True)
print(f"Number of samples: {data_train.shape[1]} / {data_test.shape[1]}")

new_policies = normalize_policies(data_train[0], data_train[1])

train_set = TemplateDataset(data_train[0], new_policies, data_train[2], training=True)
test_set = TemplateDataset(data_test[0], normalize_policies(data_test[0], data_test[1]), data_test[2], training=False)


args = TrainingArgs(
    train_epochs=8,
    batch_size=500,
    print_progress=True,
    # from_pretrained="../models/model_0.pth",
    model_output_path="../models/model_2.pth"
)
trainer = Trainer(model=NaiveNet(ROW_COUNT, COLUMN_COUNT),
                  train_dataset=train_set,
                  test_dataset=test_set,
                  training_args=args
                  )

trainer.train()
