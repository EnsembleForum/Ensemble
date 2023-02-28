
# The Ensemble Frontend

The frontend is built upon NodeJS as our runtime environment, with npm used to manage packages and React and TypeScript to build the UI.

## React - Web Framework

We used [React](https://reactjs.org/), as it is a popular framework and our
frontend developers were already familiar with its usage due to COMP6080.
React is a solid framework as it allows us to update the state of our
application using the virtual DOM, so we don’t ever need to reload the page to
display changes to the user on the frontend. On top of this, it allows us to
reuse components across our application, which sped up our development process
and consistency in styling across pages. The cons of using purely React as
opposed to using React with a framework such as Redux or Next.js, is that we
have to manually fetch from the backend server to display changes on the
frontend, rather than rendering changes to the frontend when the database
updates. However, using Redux or Next.js would have introduced an additional
layer of complexity to build out for our application that no-one had
experience using.

## TypeScript - Programming Language

We elected to use [TypeScript](https://www.typescriptlang.org/) over
JavaScript, as it helped us to guarantee an additional layer of type safety
for our code, which made it easier to prevent complex bugs in our code.
Typescript requires all data used in our frontend code to be typed. This made
development slower as we had to type all of our data, but as the scope of the
frontend grew, Typescript helped us to immediately catch and fix type-related
issues and errors as they occurred when we coded them, rather than running
into unknown errors with unsafe types as are common in JS development.
Additionally, this allows for ease of development, as we can see, for example,
what types a function’s parameters are or what types an object is composed of
without having to write extensive documentation.

## Jest - Testing Framework

We initially intended to write tests for our frontend code using
[Jest](https://jestjs.io/), but owing to time constraints, our frontend
developers decided that it would provide very little benefit for a lot of time
commitment. Our decision to set up tests ended up being a massive time
commitment, as the fact that we needed to contain the frontend and backend in
the same repository meant that the setup process was extremely difficult and
frustrating, which delayed our work on the website significantly.  In
retrospect, we should have avoided frontend testing as they caused us to spend
weeks without having a functional frontend. To make up for this, we made sure
that the backend developers tested all the expected behaviour of each piece of
frontend functionality before each merge, and in this way caught any errors
that may have occurred.

## Styling

We used a package called [Theme UI](https://theme-ui.com/) to theme our
frontend. This is a very un-opinionated styling framework which allows us to
style all of our components in a consistent manner and add our own effects
rather than relying on third party animation like material UI. We also used a
package called styled-components which allowed us to write CSS styling for
individual react components directly in the typescript files where they are
implemented. This made styling far more consistent and improved readability
and ease of use for developers when writing styles for components, as there
are no external CSS stylesheets involved.

## Software Layout

We structured our folders in such a way that the frontend folder was in the
base folder of our repository, which allows us to run the start frontend
command from the base folder (npm start). The base layer of our frontend
folder contains setup for jest testing, our base App and index.tsx files that
render the page, as well as our typescript interfaces. Inside the pages folder
are the main pages that we render (browse, admin, login, etc.), and inside the
pages/components folder are any smaller components (buttons, navbar, etc.) that
our pages use.
