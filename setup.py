import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
    name="ezslack",
    version="0.1.2",
    license="MIT",
    author="taekop",
    author_email="taekop@naver.com",
    description="Easy Slack framework wrapping Bolt for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/taekop/ezslack",
    packages=setuptools.find_packages(),
    keywords="slack",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "slack-bolt>=1.18.0",
        "slack-sdk>=3.27.0",
    ],
    python_requires=">=3.9,<4.0",
)
