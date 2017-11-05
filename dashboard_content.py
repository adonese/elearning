"""
This module is used to store __all__ of the website links. To keep very simple, the structure is as follwoing:
topic: (course_name, course_url), which then get viewed on `dashboard navs`.
"""

def dashboard():
    CONTENT_DICT = {"GIS":[("Introduction to GIS", "/introduction-to-gis"), 
    ("GIS on the Web", "/gis-on-the-web"), ("GIS Analysis", "/gis-analysis")],
    "SCIENTIFIC COMPUTING": [("Intro to Programming", "/programming-101"), 
    ("Intermediate Programming in MATLAB", "/intermediate-matlab")],
    "DATA ANALYSIS": [("Intro to Scientific Python Stack", "/intro-to-scientific-python")],
    "ANDROID": [("Java 101", "/java-101", "Building Android Applications using Android Studio", "/building-android-applications")]
    }
    return CONTENT_DICT