import setuptools

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="flasktodo",
    version="0.0.1",
    authors="Steve Eckles and Kevin Lueke",
    ##author_email="zachfedor@gmail.com",
    url="https://github.com/kevinlueke/flask-todo",
    description="A simple to-do application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['flask', 'psycopg2'],
    tests_require=['pytest'],
    python_requires='>=3.6',
)

