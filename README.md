# Restaurant-Recommender-based-on-ratings-and-nearness-using-Pearson-Correlator
<h3>Problem Description</h3>
<p>Simulate 1000 visits to the provided 15 restaurants, and provide visualizations showing frequency that each restaurant is visited, their distance, and the rating that the algorithm calculated for missing restaurant.</p>

<h3>Implementation</h3>

The problem is divided into 3 parts:
<ol>
<li>Calculate the distance of the restaurant</li>
<li>Calculate the missing rating of the restaurant</li>
<li>Simulate 1000 visits favoring restaurants with high ratings and less distance</li>
</ol>

<h3>Calculating the distance of the restaurant</h3>

The users location is considered to be at Origin(0,0). The distance of each restaurant is calculated using the Euclidean distance formula.

<img src="https://github.com/NandanNayak/Restaurant-Recommender-based-on-ratings-and-nearness-using-Pearson-Correlator/blob/master/euclidean_distance_algoritm.png" />

<h3>Calculating the missing rating of the restaurant</h3>
<p>To calculate the missing rating of the restaurant, a similarity has to be determined between items. This is calculated using the Pearson Correlation equation. The Pearson correlation gives an numerical value about how similar is item j to item i.</p>
<img src="https://github.com/NandanNayak/Recommender-System-using-Item-Based-Collaborative-Filtering/blob/master/Pic1.png" />

<p>Where Wi,j is the Pearson Correlation between item i and j. U is the set of co-rated users.
The missing rating is then predicted using the equation given below.</p>
<img src="https://github.com/NandanNayak/Recommender-System-using-Item-Based-Collaborative-Filtering/blob/master/Pic3.png" />
<img src="https://github.com/NandanNayak/Recommender-System-using-Item-Based-Collaborative-Filtering/blob/master/Pic2.png" />

<h3>Simulating 1000 visits favoring restaurants with high ratings and less distance</h3>
<p>A restaurant of a given rating is given weightage based on the distance. Lower the distance, higher the weightage. The weightage is given in the form of an interval. The range of the interval is higher to represent higher weightage for a restaurant.</p>

<p>For eg. :
{1: [['E', '0.62'], ['M', '1.27'], ['O', '1.25'], ['N', '2.37']], 
2: [['G', '1.56'], ['F', '1.48'], ['H', '1.10']], 
3: [['D', '1.15'], ['J', '0.28']], 
4: [['C', '2.50'], ['B', '1.97'], ['I', '1.58'], ['K', '0.92'], ['L', '1.83']],
5: [['A', '1.33']]}</p>

<p>The above dictionary contains a set of restaurants with their distance for each rating.
This is converted into a weighted interval as shown below.</p>

<p>{1: [['E', 5], ['O', 9], ['M', 12], ['N', 14]], 
2: [['H', 4], ['F', 7], ['G', 9]], 
3: [['J', 3], ['D', 5]], 
4: [['K', 6], ['I', 11], ['L', 15], ['B', 18], ['C', 20]], 
5: [['A', 2]]}</p>

<p>So considering a rating of 4, there are 4 restaurants <em>K,I,L,B</em> and <em>C</em>. Since <em>K</em> has the lowest distance among all the 4 rated restaurants, it has the highest interval i.e. from [0,6] which gives a higher weightage. <em>I</em> gets an interval of [7,11], <em>L</em> gets [12,15], <em>B</em> gets [16,18] and <em>C</em> gets [19,20]. Now a random is generated between 0 and 20. The restaurant is selected based on the interval the random number belongs. In this way, <em>K</em> has the highest probability of getting picked. Therefore this approach favors nearest restaurant.</p>

<p>Similarly, the restaurants with high ratings have higher weightage by giving them larger interval. A number is randomly generated between 0 and 20. 5 star restaurants have [0,6] interval, 4 stared one’s have [7,11], 3 stared one’s have [12,15], 2 stared one’s have [16,18] and 1 stared one’s have [19,20] interval. Therefore this approach favors restaurant with high rating.</p>

<h3>Execution</h3>

The command to execute is as follows:
<strong><em>python nayak_nandan_recommender.py (neighborhood)</em></strong>
<p>neighborhood : This parameter determines as to how many ratings in the neighborhood  are to be considered to predict a missing rating for a restaurant</p>

eg.<strong><em>python nayak_nandan_recommender.py 4</em></strong>

<h3>Results</h3>
<p>For the above command, the following graph was generated during one execution.</p>
<img src="https://github.com/NandanNayak/Restaurant-Recommender-based-on-ratings-and-nearness-using-Pearson-Correlator/blob/master/Graphical_Output.png" />
<p>The first subplot represents <em><u>Distance against Restaurants</u></em>. The second subplot represents <em><u>Restaurant Ratings against Restaurants</u></em> and the third subplot represents <em><u>Frequency of visits against Restaurants</u></em>. The graph clearly shows that the nearby restaurants with high ratings are highly favored which gets reflected in the higher visits.</p>
