'''
Copyright (c) 2023 Raunak Verma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This Program accesses ONLY publically available data, which is protected by the U.S Ninth Circuit of Appeals Ruling,
which found that scraping data that is publicly accessible on the internet is NOT a violation of the 
Computer Fraud and Abuse Act, or CFAA. 

By using this program, you agree to Twitter's Terms of service listed at https://twitter.com/en/tos
and assume full responsibility for abiding by those regulations.
'''


# Change the Variable below to "YES" in order to use the code. This Method makes it so absolutely no code will work without the express agreement from the user.


access = "NO"


# Run Main Program if the user agrees to the terms
if access == "YES":
    
    # Import Modules
    from apify_client import ApifyClient # To download, use pip install apify-client
    from googleapiclient import discovery # To download, use pip install google-api-python-client
    import time
    import json

    # Get input to see which user to analyze
    user = input("Enter the twitter handle of the public figure you would like to analyze: ")
    
    print("Please wait as the program processes your data. This may take up to 60 seconds...")

    for i in range(2):
        print()


    # Initialize Clients with the Necessary API Tokens
    client = ApifyClient("<YOUR APIFY KEY>") # You can find your key after creating an apify account on apify.com by going to settings > integrations > personal api tokens and copying the token.
    google_key = '<YOUR GOOGLE PERSPECTIVES API KEY>'  # In order to get a Google Perspectives API Key, refer to this article: https://developers.google.com/codelabs/setup-perspective-api#0
    service = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=google_key,
    discoveryServiceUrl=
    "https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

    # Define Functions
    def inflammatory_index(text):
        try:
            # Analyze the provided text
            analyze_request = {
                'comment': {'text': text},
                'requestedAttributes': {'INFLAMMATORY': {}}
            }

            response = service.comments().analyze(body=analyze_request).execute()

            # Get the inflammatory score
            inflammatory_score = float(round(response['attributeScores']['INFLAMMATORY']['summaryScore']['value'],3))

            return inflammatory_score
        
        # In case the post content cannot be analyzed for toxicity (due to reasons like emojis or other unparsable text), return a notice.
        except Exception:
            return ("This comment was non-parsable and the value is unknown.")
        
    # Initialize an empty list to store all scraped data. This will be useful when we convert our data to a json file.
    
    scraped_data = []

    # Prepare the Actor input for Apify
    run_input = {
        "handles": [str(user)],
        "tweetsDesired": 100 ,
        "proxyConfig": { "useApifyProxy": True },
    }

    # Run the Actor and wait for it to finish
    run = client.actor("quacker/twitter-scraper").call(run_input=run_input)

    # Fetch and print results
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        tweet = item["full_text"]
        retweets = int(item["retweet_count"])
        followers = int(item["user"]["followers_count"])
        date = item["created_at"]
        
        # Print the Formatted Output

        print(f"Date Posted: {date[:10]}")
        print(f'Post Content: "{tweet}"')
        
        # Except Situations where the Inflammatory Content Index Was Unknown
        try:
            print(f"Inflammatory Content Index: {round(inflammatory_index(tweet)*100)}%")
        except Exception:
            print(inflammatory_index(tweet))

        print(f'Post Shares: {retweets}')
        print(f"Follower Count: {followers}")
        print(f"Post Shares to Followers Ratio: {round(retweets/followers*100,10)}%")  

        for i in range(2):
            print()
        time.sleep(1)

        # Append the scraped data to the list as a dictionary
        scraped_data.append({
            "Post Time": date,
            "Post Content": tweet,
            "Inflammatory Content Index": inflammatory_index(tweet),
            "Post Shares": retweets,
            "Follower Count": followers,
            "Post Shares to Followers Ratio": round(retweets/followers,3)
        })

    # Save the scraped data to a JSON file, where it can be opened by a JSON viewer or interpreted by other machines.
    output_file = f"user_scraped_data.json"  # Create a filename. You can make this unique by putting {user}, but to respect the privacy of the user in the output file we will not include their handle and rather use a very generic filename.
    with open(output_file, "w") as json_file:
        json.dump(scraped_data, json_file)
       
else:
    print("In order to use this program, you must change the access variable in line 4 to yes. Please ensure you have read all the terms outlined above before proceeding.")


print("This is the end of the program. If you agreed to the access variable and received no output, it is likely that you did not input a valid user. Please try again!")
