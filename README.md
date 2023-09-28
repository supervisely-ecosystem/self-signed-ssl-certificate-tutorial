<!-- # Self signed SSL certificate tutorial -->
# Fixing SSL Certificate Errors in Supervisely

## Introduction

SSL certificate errors can occur when you're working with the Supervisely SDK and the server uses a self-signed certificate.

```json
{
   "message": "Temporary connection error, please wait ...:  Retrying (1/10).", 
   "method": "users.me", 
   "url": "https://my.company.com/public/api/v3/users.me", 
   "details": "HTTPSConnectionPool(host='my.company.com', port=443): Max retries exceeded with url: /public/api/v3/users.me (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1131)')))", 
   "timestamp": "2023-09-28T18:24:48.664Z", 
   "level": "warn"
}
```

In such cases, your code may not have the necessary certificate chain to validate the certificate provided by the server. This tutorial will guide you through the steps to resolve this issue by adding the certificate chain to the trusted store of your HTTP client.

**Note:** Disabling SSL checks is not recommended for security reasons, so it's best to add the certificate chain.

## Options to Fix SSL Certificate Errors

### Option 1: Supervisely SDK (Recommended)

#### Step 1. Create .env file with SLY_EXTRA_CA_CERTS variable

Create a `.env` file in the same directory as your code and add the following line to it:

```text
SLY_EXTRA_CA_CERTS=/path/to/certificate-chain.crt
```

In our example it's `local.env` file

#### Step 2. Test Your Connection

After creating a `.env` file with `SLY_EXTRA_CA_CERTS` variable, test your connection to the Supervisely server using the SDK. Supervisely SDK will automatically add your certificate to the bundle. If you've set the environment variables correctly, you will see this message in the terminal:

```json
{
   "message": "Certificates were added to the bundle: my_company_ca.crt",
   "timestamp": "2023-09-28T20:35:55.646Z",
   "level": "info"
}
```

```python
from os.path import expanduser
from dotenv import load_dotenv

# load env files before importing supervisely
load_dotenv("local.env")
load_dotenv(expanduser("~/supervisely.env"))

import supervisely as sly

api = sly.Api.from_env()

# If you've set the environment variables correctly, you should be able to connect to the server
# Your code to interact with Supervisely goes here, send any API request, for example request user info
user = api.user.get_my_info()
print(user.login)
```

### Option 2: CLI

**Note:** Supervisely SDK uses HTTP client library `requests`. If you are using a different HTTP client, please refer to its documentation for instructions on how to add a certificate chain.

#### Step 1. Locate the Certificate Bundle

If you already have a working certificate bundle on your machine, it is often found in `/etc/ssl/certs/ca-certificates.crt` on Linux systems.

You can use this bundle directly or concatenate the certificate chain with it to create a new bundle.

#### Step 2. Concatenate the Certificate Chain (if needed)

If you need to create a new bundle, first obtain the certificate chain.

Concatenate the certificate chain and the ca-certificates file into a new bundle file using a text editor or command line tools. For example, you can use the `cat` command on Linux:

```bash
cat /path/to/certificate-chain.crt /etc/ssl/certs/ca-certificates.crt > /path/to/new-bundle.crt
```

#### Step 3. Set the REQUESTS_CA_BUNDLE Environment Variable

To pass the certificate bundle to the Supervisely SDK (which uses the Requests library under the hood), set the `REQUESTS_CA_BUNDLE` environment variable to the path of your new bundle.

```bash
export REQUESTS_CA_BUNDLE=/path/to/new-bundle.crt
```

#### Step 4. Test Your Connection

After setting the environment variables, test your connection to the Supervisely server using the SDK. Your code should now be able to validate the server's self-signed certificate.

```python
from os.path import expanduser
from dotenv import load_dotenv
import supervisely as sly

load_dotenv(expanduser("~/supervisely.env"))

api = sly.Api.from_env()

# If you've set the environment variables correctly, you should be able to connect to the server
# Your code to interact with Supervisely goes here, send any API request, for example request user info
user = api.user.get_my_info()
print(user.login)
```

**Note:** if you're using `urllib`, either directly or indirectly (`pytorch` or some other library), don't forget to set `SSL_CERT_FILE` environment variable.

```bash
export SSL_CERT_FILE=/path/to/new-bundle.crt
```
