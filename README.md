### VISUAL ANALYSIS OF MOBILE SENSING TIME-SERIES DATA: IDENTIFYING INDIVIDUAL AND RELATIVE BEHAVIOURAL PATTERNS ![visitors](https://visitor-badge.glitch.me/badge?page_id=mohd-muzamil.flaskDashboard)
Master's thesis project <B>Demo</b>(Will soon deploy this system with dummy data on Heroku)

### Abstract
Mental well-being is increasingly demanded due to growing concerns about mental
health. At the same time, the Internet and smartphones are transforming the world
in unprecedented ways. This pervasiveness opens up new avenues for research by
providing access to an individual’s behaviour and daily habits. Unobtrusive data
collection and analysis from smartphone sensors is a promising approach to addressing
mental health issues and have been the focus of many research studies. In this
work, we explore this opportunity by analyzing data collected from smartphone usage
and leveraging the advantages of data visualization and machine learning methods
to possibly identify and compare behavioural indicators and patterns that can indicate
mental health. We developed a visualization system to interact with extracted
features about behavioural indicators like screen usage, calling, and sleep to assess
the daily routine of participants under study. We also present two usage scenarios to
demonstrate our visual approach’s applicability in exploring the given dataset.

[Thesis_report](https://dalspace.library.dal.ca/handle/10222/81757)

#### Snapshot of the Visualization system:
![image](https://user-images.githubusercontent.com/19529402/176933948-6d9ca602-e3ff-4303-a4da-9ba81d823597.png)

#### Tech Stack
<table>
    <thead>
        <tr>
            <th>Sl no</th>
            <th>Architecture</th>
            <th>Tech</th>
            <th>Usage description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td rowspan=5>Front-end</td>
            <td>HTML/CSS/JavaScript</td>
            <td>User Interface(UI) development</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Bootstrap</td>
            <td>Input section features</td>
        </tr>
        <tr>
            <td>3</td>
            <td>bootstrap-multiselect</td>
            <td>Dropdown selection feature</td>
        </tr>
        <tr>
            <td>4</td>
            <td>d3.js</td>
            <td>Custom charting/Visualization</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Jquery</td>
            <td>Event handling and client-server data connectivity</td>
        </tr>
        <tr>
            <td>6</td>
            <td rowspan=4>Back-end</td>
            <td>Python3</td>
            <td>Data preprocessing and data manipulation at Back-end</td>
        </tr>
        <tr>
            <td>5</td>
            <td>pandas</td>
            <td>Data preprocessing and feature Engineering</td>
        </tr>
        <tr>
            <td>5</td>
            <td>scikit-learn</td>
            <td>Implementation of ML algorithms</td>
        </tr>
        <tr>
            <td>5</td>
            <td>[Distance Grid(DGrid)](https://github.com/fpaulovich/dimensionality-reduction.git)</td>
            <td>Removal of overlap in glyphs</td>
        </tr>
    </tbody>
</table>
