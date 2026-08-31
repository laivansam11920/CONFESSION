```javascript
function sendDataToSever(e) {
  var formResponse = e.response;
  var itemResponses = formResponse.getItemResponses();
  
  var data = {};
  for (var i = 0; i < itemResponses.length; i++) {
    var itemResponse = itemResponses[i];
    var title = itemResponse.getItem().getTitle();
    var answer = itemResponse.getResponse();
    data[title] = answer;
  }
  
  var url = 'https://confession-pdsi.onrender.com/submit-confession-form'; 
  
  var options = {
    'method': 'post',
    'contentType': 'application/x-www-form-urlencoded',
    'payload': data
  };
  
  UrlFetchApp.fetch(url, options);
}
```