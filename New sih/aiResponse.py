import google.generativeai as genai
from flask import Flask, render_template, request, flash, redirect, url_for, session

import random

#model ready
genai.configure(api_key='Api_Key')
model = genai.GenerativeModel(model_name="gemini-pro")

#greeting
greetingL = [
    "Hello, this is KISAAN AI, how can I help you today?",
    "Greetings! I'm KISAAN AI, ready to assist you.",
    "Nice to meet you! I'm KISAAN AI. How can I be of service?",
    "KISAAN AI at your service. How can I help you today?",
    "Good day! This is KISAAN AI. What can I do for you?"
    ]



