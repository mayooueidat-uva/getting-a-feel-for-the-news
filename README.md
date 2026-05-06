# DS 4320 Project 1: Getting a Feel for the News
**Executive Summary**:<br> 
**Name:** Maya Uwaydat<br>
**NetID:** zvd6vz<br>
**DOI:**<br>
**Press Release:** press_release<br> 
**Data:** data_files<br>
**Pipeline:** load_clean transform_analysis<br> 
**License:**<br>
*Note: This project builds upon [a project I did last semester](https://github.com/mayooueidat-uva/mayas-sensational-project/blob/main/README.md). The previous project focused on correlations between the evolution of communications technology and the sensationalisation of New York Times headlines; this project focuses correlates sentiment and word choice with media reliability across news sources. The domain is the same, but the project aims are different.*<br>
## Problem Definition 
### General problem and refined specific problem statement
- General problem statement: We want to easily detect poor-quality news just from reading the headline.
- Refined problem statement: With the progression of communications technology, misinformation spreads at an increasingly rapid pace.  Therefore, we must investigate whether we can predict the reliability of an article containing strong emotions in its headline. If strong correlations between the absolute value of headline sentiment and reliability are found, one could design applications to detect potentially misinformative articles.
### Refinement Rationale 
Because I am trying to quantify "news quality" and cannot parse through news sources manually, I must rely on a media-quality aggregator. I decided to use news outlets' Ad Fontes Media media-quality scores, which seem to be calculated manually and not algorithmically. A panel consisting of one left-leaning, one right-leaning, and one centrist reviewer are assembled to review articles for both "bias" (where they lie on the political spectrum) and "reliability" (which measures whether articles contain reliable information, and how much they rely on fact versus opinion). The metric I am focusing on is "reliability," as I deliberately left out political bias from my metric of quality. The topics and opinions expressed in articles are used to calculate bias values; for example, an article describing climate change's effects on certain communities might be marked as heavily left-leaning, even if its contents are accurate and its arguments are constructive.  
### Motivation 
As users of the Internet, we are forced to tolerate a constant barrage of information, and a decent proportion of it is not worth our time (at best) or created with malicious intent (at worst). People do not have the expertise or time to individually fact-check every news article for themselves, so I had the idea of creating an algorithm that would be used by an application to *predict* news accuracy quickly. I would like to note that I don't imagine that the model built in this project will actually be useful in practise; it is just a prototype, but it could potentially be used to build a more sophisticated, accurate model.<br>
### Getting a Feel for the News: Sentiment Analysis and Article Reliability
## Domain Exposition 
## Data Creation
## Metadata
