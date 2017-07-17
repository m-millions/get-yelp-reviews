# get-yelp-reviews
Get a specified number of yelp reviews - Client and API

(1) Create a Yelp app to get a client ID and Secret and update in the API file:
--->>> https://www.yelp.com/developers/documentation/v3/authentication

(2) Install dependencies in requirement.txt (use of a virtual environment is recommended but not necessary )

(3) Install Curl so that we can see the API JSON response on the console:
--->>> https://curl.haxx.se

(4) Make sure "get-yelp-reviews-API.py" is in executable mode and run:
--->>> chmod a+x get-yelp-reviews-API.py
--->>> python get-yelp-reviews-API.py

(5) Launch webbroser and type:
--->>> http://localhost:5000

NOTE: The API end-point requires authentication.  You can change the hardcoded credentials at will.
Using hardcoded credentials for a PRODUCTION release is not the recommended approach; it is being done here purely for example purposes.

(6) Run the following at the command line:
```
curl -u claudia123:reviews123 -i http://localhost:5000/get-reviews/api/v1.0/reviews/pizza/New+York,+NY/Juliana\'s+Pizza/5
```
(7) Smile. It worked!


Sample JSON response:
```
{
  "name": "Juliana's Pizza",
  "reviews": [
    {
      "rating": "5.0 star rating",
      "review": "Many may think pizzas may taste the same whether it is purchased at a Dominos, Costco, or at a Juliana. Well, that is not the case as your original thoughts on pizza will change when you try Juliana's! \n\nAmazing experience that you can share with your friends, family, and loved ones. We walked the Brooklyn Bridge from Lower Manhattan to cross to Brooklyn. Once we were there, it started to heavily pour rain in which we quickly hailed Lyfts to make it. Despite the rain, the line was pretty long. Our party 8 was eventually seated and off we go\n\nOrdered \n- Housemade meatballs (5/5). Beautiful. The sauce was delicious and it is recommended to cut the the meatballs in halves for easy sharing. I cannot imagine how this would taste if made into a spaghetti\n- Margherita Pizza (4.5/5). Classic tomato, mozzarella and basil style pizza\n- No. 4 (4.5/5). Amazing pizza with tomato, mozzarella, arugula and prosciutto\n- No. 6 (5/5). To die for! Toppings consist of grilled chicken with tasty housemade guacamole and cilantro \n\nBest Pizza in NYC and one of my favorite dining experiences overall. A must try whenever you're in NYC / Brooklyn"
    },
    {
      "rating": "4.0 star rating",
      "review": "Made our way in here after a walk across the Brooklyn Bridge. Located right next to Grimaldi's, both places have lines out the door. I don't think the time of day matters because this place seems like it's busy all day and everyday. My group of five ordered two salads, 2 small pizzas, and an order of meatballs. Our arugula salads were fresh but overdressed. The meatballs (3 per order) were moist, tender, and had a healthy amount of tasty gravy. The pizzas were that perfect combination of crispy and chewy with just a touch of char from the coal ovens. Looks like they boast some of New York's best egg creams but we opted for bottled cokes (little bottles). \nService was very friendly and prompt but we were not given enough settings/silverware and had to wait for them while our food was on the table. We also had to ask for water refills and when our server refilled waters the pitcher was leaking water all over our pizza. He saw it and we brought it to his attention but he just said \"Sorry\" and wouldn't stop pouring the waters,via leaky pitcher, over our food. My friend instinctively put her hand underneath to stop our pizza from getting soaked but another one of us finally moved our food out of the way since our server obviously didn't care. Seriously guy? One extra body movement or even having us hand you our glasses would have rectified that easily..but hey I guess water logged pizza is acceptable.\nDespite the service hiccups we thought the place was a great little spot.\n The host was delightful and made sure we all took the right trains and went to the proper subway stations since we were going in three different directions. Thanks for the transit help. I'd recommend it to friends who are in that part of Brooklyn."
    },
    {
      "rating": "1.0 star rating",
      "review": "Worse customer service ever. The manager doesn't care anything about people's needs. Food is average (not good not bad), but waiting time is a pain, it just doesn't worth it. \n\nIf you are looking for a place to have a good day, avoid coming here."
    },
    {
      "rating": "4.0 star rating",
      "review": "Brooklyn Pizza!! \nWow!! Looooong lines for Juliana's Pizza in the raining evening.... We gave up waiting line and takeout Pizza instead!! Since we stayed really close @1 Hotel Brooklyn!! \nWe takeout Salad and Half Margarita and White pizza with prosciutto!! \nPizza was pretty good but I wouldn't want to wait over hour for this pizza. I know better pizza places in Japan!!"
    },
    {
      "rating": "5.0 star rating",
      "review": "Given there is no shortage of quality pizzerias in NYC it may seem absurd to wait in line for one - but honestly, Juliana's is well worth it. \n\nWe went around 4pm on a Saturday and the line was beyond the cordons they have set up. In the end we waited about 45 mins, which is not that bad (when you compare to say waiting 2hrs for a milkshake at Black Tap or the Dumbo ride at Disney...). It's well organised and they check the party sizes in the line so that they can arrange the tables accordingly. \n\nOnce seated it's relatively cosy but not to the point where other tables are interfering with your enjoyment. The walls (or at least the one I was looking at) are covered in pictures of Sinatra. \n\nYou have a choice of classic pizzas that you can add extra toppings or their specialties, to which you can make no changes. We went for a Margherita with pepperoni (wife's pick) plus the No. 1 special (a white pizza with mozzarella, scamorza affumicata and pancetta). Both were great but the special was the stand out dish - so good - best pizza I've had. Didn't have specs for one of their \"sweets\" as we had two larges and I was stuffed - but I had the Brookie bridge (ice cream sandwich with brownies) a couple of years ago and if i remember correctly it was great. \n\nGotta shout out to our waiter Trimell - not just for being a great waiter, but also while we were waiting in line he ran after a customer that had left their card behind"
    }
  ],
  "uri": "http://localhost:5000/get-reviews/api/v1.0/reviews/pizza/New%20York%2C%20NY/Juliana%27s%20Pizza/5"
}
```
