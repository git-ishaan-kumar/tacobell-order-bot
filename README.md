# Taco Bell Order Bot

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?logo=google&logoColor=white)

A simulation of a chat bot that takes Taco Bell orders. Users can add, remove, and edit items on their order using a mock Taco Bell menu.

[![Live Demo](https://img.shields.io/badge/LIVE_APP-tacobell--order--bot.streamlit.app-FF4B4B?style=for-the-badge&logo=streamlit)](https://tacobell-order-bot.streamlit.app/)

---

## A Look Inside

![Taco Bell Order Bot Screenshot](./static/cover.png)

## Video Demo
[![Pooja Room Demo](https://img.shields.io/badge/YouTube-Watch_Demo-FF0000?logo=youtube&style=for-the-badge)](https://youtu.be/vuFtQ1dv88o)

---

## Features
* **Chat Bot:** Powered by Google's Gemini API to act like a real Taco Bell cashier.
* **Cart Management:** You can add, swap, or completely remove items, and the bot will update its internal memory.
* **Menu Integration:** The bot is tied to a mock Taco Bell menu.
* **Customizations & Sizes:** You can upgrade items (e.g., make it "Supreme") or specify sizes for drinks.
* **Automated Receipt:** Once ready to checkout, the bot calculates the total price and generates a clean, structured JSON receipt.

## Technologies
* **Programming Language:** Python
* **GUI Integration:** Streamlit
* **LLM:** Google Gemini (`gemini-3.1-flash-lite`)