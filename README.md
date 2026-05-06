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
### Terminology table 
| Bias  |   In the context of this project, a "biased" news source or article has<br> strong political leanings (towards either end of the spectrum).<br> I will NOT be using "bias" the same way I use "cognitive bias" or <br>"confirmation bias." |
| Cognitive Bias | Mental shortcuts that lead to errenous thinking; includes believing<br> in the most widely-available information, listening only to certain<br> sources, etc.|
| Confirmation bias | Susceptibility to believing information/drawing conclusions that<br> affirm previously-held beliefs; a type of cognitive bias |
| Reliability (`reliability_score`) | The reliability score of an article or news source as calculated by<br> panelists at Ad Fontes Media   |
| VADER score (`vader_score`)  | A score from 1 to -1 gauging the strength of emotions expressed<br> in a piece of text, as decided by the VADER sentiment analyser.<br> -1 means negative sentiment; 0 means neutral sentiment; 1 means<br>positive sentiment.  |
### Domain description 
### Background reading 
Check the GitHub repo and read the instrux *ON THE README IN THE BACKGROUND READINGS FOLDER:* (placeholder)
### Reading summary table
| Article Title | Article Format | Article Content | Link |
| -------- | ------- | ------- | ----- |
| Media Content Analysis: Its Uses,<br> Benefits and Best Practice Methodology  |  Academic Periodical   | Used to better understand the importance of media analysis (which is<br> part of my motivation for this project). It was published 20 years ago, but it<br>still contains meaningful research about the effects of mass media. | [placeholder](https://www.researchgate.net/publication/267387325_Media_Content_Analysis_Its_Uses_Benefits_and_Best_Practice_Methodology) |
| Research Methods for the Creative Arts... | Web Article  | Used to briefly understand the domain of my project (i.e. media analysis)<br> and provides a list of questions I must ask when engaging  with news media. | [placeholder](https://ecu.au.libguides.com/research-methodologies-creative-arts-humanities/media-analysis)  |
|Understanding Viewer Opinions: Sentiment<br> Analysis on Movie Review using VADER and<br>LSTM Model | Academic Periodical | An article studying the difference in effectiveness of LSTM and VADER<br> sentiment analysis models on assessing emotions conveyed in movie<br> reviews. Used to better understand VADER and its own biases. | [placeholder](https://science.utm.my/procscimath/wp-content/uploads/sites/605/2024/09/1-8-AHMAD-DANIEL-BIN-AZAHREE-A20SC0005.pdf) |
| Cognitive biases in news-making and fact<br>checking: a mixed methods approach| Web Article | Article on how cognitive bias is involved in fact-checking; goes into<br>depth about different froms of cognitive biases. Used for background<br>research on biases present in gauging "reliable" news. | [placeholder](https://edmo.eu/blog/cognitive-biases-in-news-making-and-fact-checking-a-mixed-methods-approach/) |
| (no title) | Interactive Chart | Ad Fontes Media's interactive chart; plots media outlets based on their<br> reliability and their bias. Logos for outlets can be clicked for more in-depth<br> assessments.| [placeholder](https://app.adfontesmedia.com/chart/interactive?utm_source=adfontesmedia&utm_medium=website)
| Methodology | Web Article | Provides a description of Ad Fontes Media's methodology for assessing<br> the quality of news. Used to understand the metric I'm using and also for<br>bias mitigation.| [placeholder](https://adfontesmedia.com/methodology/) |
Methodology - White Paper | Report | A more in-depth description of Ad Fontes Media's methodology and rater<br> qualifications. Used for a more comprehensive understanding of scoring<br>metrics.| [placeholder](https://adfontesmedia.com/methodology-white-paper/)
Comparative Analysis of VADER and Textblob<br>on Financial News Headlines | Academic Periodical | Compares VADER and Textblob, two popular sentiment analysis tools.<br> Used to select which to use for the project. | [placeholder](https://jds-online.org/journal/JDS/article/1441/info)
Top 50 US News Websites: Double-digit YoY<br> declines at more than half despite the Iran<br>war | Web article | A March 2026 assessment of US website visits to different news sources<br>that was used as a guide to select what sources to use for the project. | [placeholder](https://pressgazette.co.uk/media-audience-and-business-data/media_metrics/most-popular-websites-news-us-monthly-3/)
## Data Creation
### Provenance
### Data creation table 
| File name | File description | Link | 
| --------- | ---------------- | ---- | 
load_clean | Fetches all relevant data from NewsAPI. | placeholder | 
transform_analyse | Conducts the sentiment analysis on the headlines;<br>produces the graph. | placeholder |
### Bias identification 
Both the sentiment analysis and the reliability scores attempt to quantify subjective metrics, so they are obviously coloured by the assumptions carried by their creators. VADER is a lexicon-based model, so it searches for words that correspond with intentions and intensity values as defined by its internal dictionary ([source](https://science.utm.my/procscimath/wp-content/uploads/sites/605/2024/09/1-8-AHMAD-DANIEL-BIN-AZAHREE-A20SC0005.pdf)). Therefore, it is not accomodating for words whose meanings change across contexts, and also does not accomodate for new slang. Similarly, Ad Fontes attempted to make their media quality scores (bias and reliability) as "objective" as possible by employing reviewers from all ends of the political spectrum, even though panels' biases will inevitably slide into their decisions. Though one can confirm that a source is "reliable" by cross-checking with other sources or with established scientific or historical consensus, confirmation bias still affects perceived reliability of information ([source](https://edmo.eu/blog/cognitive-biases-in-news-making-and-fact-checking-a-mixed-methods-approach/)). Ad Fontes Media also did not specify what was meant by "right," "left," and "centrist," and the panelists' supposedly neutral decisions could be skewed in a direction that *I* might see as left-leaning or right-leaning.
### Rationale 
To mitigate the effects of biases introduced by VADER, the study focuses only on articles posted in the last ten years in the United States. English would be used more consistently across limited time and space, so VADER would judge the words relatively similarly. Meanwhile, the biases introduced by Ad Fontes Media's panelists cannot be detected within the scope if this project: I do not know the names of the panelists, nor do I have enough information to quantify their bias. The hope is that the bias mitigation measures taken by Ad Fontes Media (i.e. their attempt to gather expertise across the political spectrum) is enough for the purposes of the project; future projects would utilise news reliability scores from several sources.
## Metadata
