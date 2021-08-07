# Capstone Proposal

## Fry Pan Store
My friend is manufacturing and selling a fry pan with a new design, and asked me for a website to sell them from.

## Project Overview
This will be an online store that will describe the unique capabilities of this fry pan and and why you should buy it. You will be able to see pictures and videos of this fry pan. Finally you will be able to purchase a fry pan. 

## Functionality
- Allow users to create an account
- Display pictures and videos of each of the three different fry pans
- Allow users to select style and color of fry pan they wish to purchase
- Allow the user to add and remove items from a shopping cart that will update as you click on the buttons
- Allow users to use Stripe to pay for their items
- Send the users an automated email that thier order was received and is being processed (bonus if time)

## Data Model

#### User
- First Name
- Last Name
- Email
- Phone Number

#### Order
- User (one to many)
- Order Number
- Ship Address
- Paid (stripe payment)
- Pan Ordered (one to many)

#### Pan Ordered
- Pan Style
- Pan Color
- Quantity


## Schedule
#### Week 1
- Create Database
  - Create User Table
  - Create Order Table
  - Create PanOrder Table
- Create Login and Registration Page
- Create Homepage
- Create Pan 1 detail page
- Create Pan 2 detail page
- Create Pan 3 detail page

#### Week 2
- Work on a functional shopping cart (Find a JavaScript Framework)
- Style all of the pages from week one (Bootstrap  Framework)

#### Week 3
- Learn and implement Stripe's Payment service
- Learn and implement automated email responses (bonus if time)

#### Week 4
- Fix bugs
- Get ready to present
- Deploy onto Azure
