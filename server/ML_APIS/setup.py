from setuptools import setup, find_packages

setup(
    name='ocr_model_setup',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'easyocr',  # Install the EasyOCR package
        'torch',    # EasyOCR requires PyTorch, make sure it's installed
        'opencv-python-headless',  # For image processing tasks
    ],
    entry_points={
        'console_scripts': [
            'initialize_ocr=ocr_model_setup.init_ocr:initialize_reader',  # Creates an entry point for initializing the OCR model
        ]
    },
)