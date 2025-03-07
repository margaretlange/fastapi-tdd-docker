https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions
trying this


this debugging option
echo ${{secrets.AWS_ACCESS_KEY_ID}} | sed 's/./& /g'

idk why what i was doing wasn't working before.  anyway using the short debug script is a good idea. I basically used it until I could print my passwords.
