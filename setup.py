import setuptools

setuptools.setup(
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": [f"i3egg = i3egg.egg:main"]},
    setup_requires=["twine"],
)
