from setuptools import setup, find_packages

setup(
    name="AlphaTemplate",
    version="DEV",
    description="Game engines",
    author="manu",
    author_email='manuel.fay@gmail.com',
    packages=find_packages(include=["alpha_template", "alpha_template.*"]),
    install_requires=[
        "numpy",
        "torch",
        "scipy",
        "tqdm",
    ],
    python_requires=">=3.6,<4.0",
)
