- Note: Hopefully this isn't overkill. The more automated the better for a startup, I think. At least that was my experience at my last job.

### Central secrets vault/Config store
- This time around both will be your local .bashrc or .bash_profile file.
- see secrets_and_config.txt in this folder for all the variables that will need to be set


### Repositories
- Terraform
  - aws backends for storing state
  - aws main for infrastructure
  - auth0 for infrastructure
- Fork of ollama deep researcher code
- My main app code

### Accounts needed
- Tavily account (for the algorithm)
- Openai account (for the algorithm)
- Amazon web services account (for basic infrastructure including server and database)
- google developer account (for setting up social authentication via google)
- github account (for accessing the repositories *and* for setting up social authentication for the app via github)
- auth0 account (for setting up app authentication system)
- register a domain or find one you don't mind using. I registered mmldemo.com on aws route53 and this config files worked for that setup. It may work for another setup, I'm not sure. (For route 53 signup the one gotcha was a confirmation email that kept going to my spam folder.) 

## Software needs
- Locally you'll need to be able to run docker and docker-compose 
