<h1>COINBASE AUTOMATED REGISTRATION</h1>
<hr>
<p>This is a Python application built with Playwright designed to automate the registration process on Coinbase. It allows users to streamline account creation by leveraging Playwright's browser automation capabilities. </p>

<p>The application supports custom proxies and <b>requires</b> credentials for 2Captcha to handle CAPTCHA challenges during registration and Temp Mail credentials to get code.</p>

<p><b>Important</b>: This application does not handle phone number verification (you can write the code manually). Instead, it demonstrates how the registration process can be automated while bypassing CAPTCHA and email verification hurdles.</p>

<hr>
<h2>How to Run</h2>
<p><b>1. Clone the repository.</b></p>

```
git clone https://github.com/prokann02/registrationCoinbase.git
cd registrationCoinbase
```

<p><b>2. Install Dependencies:</b></p>

```
pip install -r requirements.txt
```

<p><b>3. Install Playwright.</b></p>
<p>On Windows:</p>

```
playwright install
```

<p>On Linux:</p>

```
playwright install-deps
```

<p><b>4. Configure Arguments.</b></p>
<p>The application requires <a href="https://2captcha.com/uk/enterpage">2Captcha</a> API key, <a href="https://temp-mail.org/uk/api">temp mail</a> API key, phone number and optionally supports proxy settings.</p> 
<p>All arguments:</p>

```
--captcha-api-key OR -c <str:your_key>
REQUIRED: API key for 2Captcha.

--temp-mail-api-key OR -m <str:your_key>
REQUIRED: API key for Temp Mail.

--phone-number OR -n <str:phone_number_to_registrate>
You can enter phone number like argument or input when start the program.

--proxy-file OR -f <str:path_to_TXT_file>
If you want to use proxy, provide TXT file splitted by new lines.
```

<hr>
<h3>Example of running:</h3>

```
python main.py --phone-number +380000000000 --captcha-key 000000aa0a000f000c0e00aaa00000a0 --temp-mail-api-key 000a0aa0aa0a0a0a00a00aa0000a000aa0000a0a0a00a0000a --proxy-file proxies.txt
```
<hr>
<h3>How it works:</h3>

[![Demo](readme_sources/preview.png)](https://youtu.be/2biH7M1PRKA)

