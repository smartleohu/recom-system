import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements.txt", "r") as file:
    install_requires = file.readlines()

setuptools.setup(
    name="recom_system",
    version="0.0.1",
    author="Ruijing HU",
    author_email="ruijing.hu@ens-cachan.fr",
    description="it is a anomalies recommandation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smartleohu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=install_requires
)
