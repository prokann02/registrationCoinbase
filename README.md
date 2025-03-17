<h1>COINBASE AUTOMATED REGISTRATION</h1>
<hr>
This is a Python application built with Playwright designed to automate the registration process on Coinbase. It allows users to streamline account creation by leveraging Playwright's browser automation capabilities. 

The application supports custom proxies and <b>requires</b> credentials for 2Captcha to handle CAPTCHA challenges during registration and Temp Mail credentials to get code.


<hr>
<h2>How to Run</h2>
<p><b>1. Install Dependencies:</b></p>
<code>pip install -r requirements.txt</code>

<p><b>2. Install Playwright.</b></p>
<p>On Windows:</p>
<code>playwright install</code>
<p>On Linux:</p>
<code>playwright install-deps</code>

<p><b>3. Configure Arguments.</b></p>
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