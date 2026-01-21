# Introduction

### Central secrets vault/Config store
- This time around both will be your local `.bashrc` or `.bash_profile` file.
- See `secrets_and_config.txt` and `secrets_and_config_remote.txt` in this folder for all the variables that will need to be set


### Repositories
- Terraform
  - aws backends for storing state (gitlab)
  - aws for infrastructure (gitlab)
  - auth0 for infrastructure (gitlab)
  - github for infrastructure (gitlab)
- Fork of ollama deep researcher code (github)
- My main app code (github)

### Accounts needed
- Tavily account (for the algorithm)
- OpenAI API account (for the algorithm)
- Amazon web services account (for basic infrastructure including server and database)
- Google developer account (for setting up social authentication via google)
- Github account (for accessing the repositories *and* for setting up social authentication for the app via github)
- Auth0 account (for setting up app authentication system)
- Register a domain or find one you don't mind using. I registered mmldemo.com on aws route53 and this config files worked for that setup. It may work for another setup, I'm not sure. (For route 53 signup the one gotcha was a confirmation email that kept going to my spam folder.) 

## Software needs
- Locally you'll need to be able to run docker and docker-compose. 
