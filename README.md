<p align="middle">
<img src="https://betanews.com/wp-content/uploads/2016/08/operating-system.jpg" width=700 height=450>
</p>
<h1>Project OS</h1>
<p>
  Simulation of a taco stand called "Tacos el Franc" as an Operating System (OS).
</p>
<p>
  It is established as follows:
</p>
<ul>
  <li>
    3 Taqueros:  
  </li>
  <ul>
    <li>1 for Asada</li>
    <li>1 for Adobada</li>
    <li>1 for Others:</li>
    <ul>
      <li>
        Lengua
      </li>
      <li>
        Cabeza
      </li>
      <li>
        Tripa
      </li>
      <li>
        Suadero
      </li>
    </ul>
  </ul>
  <p></p>
  <p>
    Each taquero is considered as a Thread and can only process one order at a time. Inside a Thread's task, considering the size of the order, ingredients and priority given, are:
  </p>
  <ul>
    <li>
      Evaluate each order.
    </li>
    <li>
      Select when to put an order in "hold" and when to continue.
    </li>
    <li>
      Can "prepare" a maximum of two tacos when an order is taken or continued.
    </li>
    <li>
      Complete an order when finished.
    </li>
  </ul>
</ul>
<h2><a href="TOC"></a>Table of Contents</h2>
<div id="TOC">
  <ol>
    <li>
      <a href="#getting_started">Getting Started</a>
    </li>
    <li>
      <a href="#prerequisites">Prerequisites</a>
    </li>
    <li>
      <a href="#installation">Installation</a>
    </li>
    <li>
      <a href="#contributors">Contributors</a>
    </li>
  </ol>
</div>

<div id="getting_started">
  <h2>
    <a href="#TOC"></a>
    1. Getting Started
  </h2>
</div>
<p>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
</p>

<div id="prerequisites">
  <h2>
    <a href="#TOC"></a>
    2. Prerequisites
  </h2>
</div>
<p>
List of elements that are needed to be installed to run the code properly.
</p>
<ul>
  <li>
    <b>Python3.6 or newest version.</b>
    <p>
    The following instructions on how to install Python are in the next <a href="http://docs.python-guide.org/en/latest/starting/install3/linux/">link</a>.
    </p>
  </li>
  <li>
    <b>Pandas3</b>
    <p>To install, using the terminal, try:</p>
    <pre>sudo apt-get install python3-pandas</pre>
    <p>or</p>
    <pre>sudo pip3 install pandas</pre>
    <p>
      For more instructions you can click <a href="https://pandas.pydata.org/pandas-docs/stable/install.html">here</a>.
    </p>
  </li>
  <li>
    <b>Matplotlib</b>
    <p>To install, using the terminal, try:</p>
    <pre>sudo apt-get install python3-matplotlib</pre>
    <p>or</p>
    <pre>sudo pip3 install matplotlib</pre>
  </li>
  <li>
    <b>Boto3</b>
    <p>If you are going to read a file from an SQS server from Amazon, you will need to download boto3.</p>
    <p>To install, using the terminal, try:</p>
    <pre>sudo apt-get install pip-boto3</pre>
    <p>or</p>
    <pre>sudo pip3 install boto3</pre>
    <p>The following folder and files are needed:</p>
    <ul>
      <li>
        Create a hidden folder in the home directory called:
        <pre>.aws</pre>
      </li>
      <p>Inside this foler, add the next files:</p>
      <li>
        credentials
        <pre>
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
        </pre>
      </li>
      <li>
        config
        <pre>
[default]
region=us-east-1
        </pre>
      </li>
    </ul>
  </li>
</ul>
<div id="installation">
  <h2><a href="#TOC"></a>
  3. Installation
  </h2>
</div>
<p>
The software is designed to be installed locally (Linux). For the moment there is no version for mac OS or Windows.
</p>
To run the programm follow the next instructions:
<ol>
  <li>
    Download the folder <a href="https://github.com/LuisS96/ProjectOS/tree/master/src">src</a>.
  </li>
  <li>
    Make sure you have all to date and run the file <a href="https://github.com/LuisS96/ProjectOS/blob/master/src/TacosMain.py">TacosMain.py</a>.
  </li>
</ol>
<p>
  If any change is needed to be made you can do so in the documents that are inside the folder <a href="https://github.com/LuisS96/ProjectOS/tree/master/src">src</a>, linked to the main file 'TacosMain.py'.
<div id="contributors">
  <h2><a href="#TOC"></a>
  4. Contributors
  </h2>
</div>
<ul>
  <li>
  <a href="https://github.com/OJMS14">@OJMS14</a>
  </li>
  <li>
  <a href="https://github.com/MarioCarvajal">@MarioCarvajal</a>
  </li>
  <li>
  <a href="https://github.com/LuisS96">@LuisS96</a>
  </li>
</ul>
