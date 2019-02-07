# Eatr
As one of our team members is diabetic, it was a pain to manually log food in his diabetes monitor app while it was already being entered in another food tracking app, MyFitness pal. Wouldn't it be great it the two apps were in sync?

Eatr is our addition to the [MyFitnesspal python API](https://github.com/coddingtonbear/python-myfitnesspal) API, and the [diabetes app Nightscout](https://github.com/nightscout/cgm-remote-monitor) by enabling MyFitnesspal foods to be logged into Nightscout as well.

For reference, MyFitnesspal is a food logger app. Nightscout is a web client for viewing blood sugar, as well as an iPhone app. Pushover is an iOS, Android, Desktop? App that allows a user to hook into its API to send push notifications to themselves, or others, when their app doesn't have the ability to. 

In the case of Eatr, we don't have access to Nightscout or MyFitnesspal's actual app for modification. So the idea is to have our own python server that monitors what food has been logged in MyFitnesspal and when certain rules are violated, or met, we can send ourselves a notification on all corresponding devices that we decide to connect to Pushover.

In its current form the App looks for you to eat too many carbs and if you do that then it sends a notification to your devices to tell you to stop. The idea is that these rules can be modified to push anything and listen to anything. If you want to drink water every 40 minutes, add that rule. And if you drank water at minute 39 and updated it on the `MyFitnesspal`, have the server reset that 40 minute water timer so it doesn't still remind you. The option are limitless.

# Setup

* Download and make an account for `MyFitnesspal`, `Nightscout` (possibly more setup, Donald could you add to this part), `Heroku`, and `Pushover`.
  * General setup for all four of these should be pretty straightforward. 

* Add the credentials/tokens from all three accounts and add them correspondingly to the `configs.example.ini` file in our configs folder.
  * The token for a `user` in Pushover can be either a single user token, or you could create a Pushover Application and use that app token in its place.
  * This would allow you to send group notifications to friends, all they would need to do is make an account and use a link created by Pushover to subscribe their account to your Pushover Application

* Change the config file from `configs.example.ini` to `configs.ini` and remove the corresponding `.gitignore` portion so that when you commit and push your code to your person Heroku server it can grab the correct configurations
  * **IT IS IMPORTANT TO NOTE THAT WHEN YOU DUPLICATE OUR REPO AND PUSH YOUR CREDENTIALS/TOKENS, PLEASE MAKE SURE IT IS PRIVATE SO YOU DON'T EXPOSE THOSE CREDENTIALS PUBLICLY**

* With all of that done, you should be able to now link your Github with the duplicated and **PRIVATE** repo, make a deployment of the app from your repo to Heroku.
  * ``` heroku logs --app your-eatr-heroku-app-name --tail ``` allows your to track your Heroku app