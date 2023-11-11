# Project Proposal: Reading Owl
## Big Idea
Working on NLTK and sentiment analysis in my previous assignment led to many questions around the ability of LLM's to sort information and create new dynamics through which humans can learn. The idea with this project is to create a website where a user can input text about a certain topic, ideally controversial in nature and having several perspectives. The input will be processed and out will come a list of summary of articles that are related to the text inputed. These article are meant to provide answers to questions that were left unanswered in the input text. This process is a framework in fact-checking known as lateral reading ([useful article](https://newslit.org/tips-tools/expand-your-view-with-lateral-reading/)). **My goal is to test out lateral reading through the OpenAI API and hopefully create a program useful when doing research or planning your next tweet storm!**

**MVP**: User can input text and output is 5-8 URLs that lead to articles that delve deeper into the input text.

**Strecth Goal**: A website where user can input text or source article and ouput is 3-5 questions and answers that give a fuller picture of the topic.

## Learning Objectives
The primary purpose of the project is exploration of the OpenAI API. I am fascinated by its capibalities and this is an opportunity to play around and attempt to make something useful of it. Some technical objectives are:

- Learning to use API for multiple calls in one user input and generally learning of their capabilities.
- Building a simple dynamic website.
- Creating a finished product.

Even though I am attempting this as an individual project I am certain I will be needing collaborators in many formats, wether it be reddiors, ChatGPT, professor, or classmates. I am looking forward to learning to **leverage different types of resources** and **exploring the communities based around python and software development.**  

And finally, I would also like to come out of this project **feeling comfortable using python, and software in general, to solve problems I see around myself**. This is a big part of why I took the class, and I hope the project is a step in that direction.

## Implementation
I see it as a 3 step plan:
1. Research: I have begun with understanding frameworks for fact checking that we currently use without AI. I feel confident that lateral reading might be the most appropriate and viable but I am also considering the CRAAP test. Assuming I stick with lateral reading, I will need to research OpenAI API's ability to do multiple calls in single input and how it can be integrated with other API's. I'll need a search engine API to look for the articles, and I am planning on using Bing. I'll also need to look at how I can sort through web searches and how to select the most appropriate output URLs.
   
2. Integration: I will need to download the API's and maybe some libraries to preprocess text. The code will probably include functions to read input text, prompt OpenAI API to generate questions regarding the text, search these questions through Bing API, collect appropriate URLs, and (maybe) summarise articles. 
   
3. Website: I plan on putting this all on Flask using some CSS to make website user friendly. Here, I will need to think about the prompt for the user input and how to display output.

## Schedule
Starting from 11.10
### Week 1
  -  Finalise fact checking framework
  -  Read API documentation and explore libraries
  -  Finalise API
  -  Research prompt engineering techniques
  -  Develop prompts 
  
### Week 2
- Write down detailed code breakdown
- Code functions for integration of APIs

### Week 3
- Complete main functions
- Start coding project website

### Week 4
- Finish project website
- Write project documents

## Risks and Limitations

There are several things that I have yet to answer. Some significant questions are:
  
- Is it possible to create a prompt that leads to accurate results with varying user inputs?
- What is the best way to select appropriate web URLs for fact checking purposes?
- Can a collection of URLs be parsed to create a single summary?

Of these, the first question is the most significant. And apart from them, there are questions around technical limitations of the API's that I don't know of yet. However, most of the risks lie in the design of the project and will need to be answered early on.

## Additional Course Content
Learning more about LLMs and how to design software that emulates human frameworks would be useful.
  