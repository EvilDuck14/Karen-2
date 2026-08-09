from setuptools import setup, find_packages
import pathlib

# allows karen to be installed as a python package
setup (
    name = "karen",
    version = "2.0.0",
    url = "https://github.com/EvilDuck14/Karen-2/",
    author = "EvilDuck",
    author_email = "theevilduck14@gmail.com",

    packages = find_packages(),
    install_requires = [],
    setup_requires=["setuptools-git"],

    description = "Evaluates & categorises Spider-Man's combos in Marvel Rivals.",
    long_description = (pathlib.Path(__file__).parent.resolve() / "README.md").read_text(encoding="utf-8"),
    long_description_content_type = "text/markdown",

    project_urls={
        "Discord" : "https://discord.gg/RpQf2zVAMP",
        "Source" : "https://github.com/EvilDuck14/Karen-2/",
    },
)