# Bookmaker Odds

A project aimed at finding sure bets.

We can talk about a sure bets, when no matter which team we bet on, we will earn money anyway. This is possible thanks to the odds differences between the bookmakers. (Similar principle as in exchange arbitration)

The project consists in scrapping the odds from the flashscore site, then finds the best offer for each event and calculates the probability of successful betting from the formula (1/odds). If the sum of the probabilities for all events in the match is less than 1, we are talking about a sure bet

The data is constantly scrapped and updated in the database


<p align="center">
  <img src="demo.gif" alt="animated" />
</p>

