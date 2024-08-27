Most Sikku Kolams apps that I have seen have limitations :
- They use planar graphs. This means the user cannot dynamically draw the kolam in the way that is normally done traditionally, instead "connecting" the dots. I understand why most programmers chose planar graphs to represent kolams as it makes things more simple, but that representation inherently stops you from unleashing the artistic potential of kolams/lusona.
- They do not integrate an automatic animation. This is unfortunate as 
- They do not offer the option to translate an image or photo to a digital kolam in the app
- No share features, no "social media" like utility for people to share their creations.

This is unfortunate. Sona/Sikku Kolams are traditions that fascinate me, and I believe in using technology to perpetuate or even further tradition is the way to go!

To fix this gap, I have decided to make my own app.

Instead of planar graphs, I decided instead to use directed graphs. A "point" can be separated into 4 vertices. Vertices can connect to each other, which results to a drawing :




To enable multi-linearity, there are "layers" :

An advantage of this implementation is that one can tweak the edges more creatively. For example, you can select a vertice and ask that whatever edge there is there, be "pointy" :


My program also enables the user to scan a sikku kolam. To achieve this, I decided to train a tensorflow lite model that is shipped with the app. I understand a lot of users will probably be from third world countries and access to utilities offline is appreciated. I say that as someone that grew up in the third world as well! Users might want to scan a sona and have slow or unavailable internet,  or even limited data.

This program focuses more-so on the Tusona tradition of Angola than on Indian Sikku Kolam. Hence, there is also the integration of proverbs, stories, and explanations, even with a voice over!

Finally, users can share each others' creations on the platform in a sort of reddit-like forum. The most appreciated drawings will receive more upvotes :



I faced a problem though. In some sona drawings, there are arbitrary curves outside of the scope of the points.

For example with this one :

With the current model, the result will be much less aesthetic :

To solve this, I decided to add the option of adding invisible points that simply describe curvatures :

Possible implementations :
	1 - Invisible points are added by the user manually
	2 - we stick the the tensorflow recognition, and when the user draws outside of the scope of any point, the curve is identitfied and "invisible" points added automatically.
