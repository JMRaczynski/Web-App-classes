const request = require('request');
const jsdom = require("jsdom");

function removeEachSecondElement(arr) {
  return arr.filter((item, index) => {
    return (index % 2) == 0
  });
}

const { JSDOM } = jsdom;
request('https://www.euro.com.pl/telefony-komorkowe.bhtml', function (error, response, body) {
  console.error('error:', error); // Print the error if one occurred
  console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
  const dom = new JSDOM(body, { runScripts: "dangerously", resources: "usable"});
  amountsOfRam = Array.from(dom.window.document.getElementsByClassName("attribute-value"));
  names = Array.from(dom.window.document.getElementsByClassName("product-name"));
  prices = Array.from(dom.window.document.getElementsByClassName("price-normal          selenium-price-normal"));

  for (let i = 0; i < amountsOfRam.length; i++) {
    if (!amountsOfRam[i].textContent.includes("GB")) amountsOfRam.splice(i--, 1);
  }
  amountsOfRam = removeEachSecondElement(amountsOfRam);
  amountsOfRam = removeEachSecondElement(amountsOfRam);
  names = removeEachSecondElement(names);
  prices = removeEachSecondElement(prices);

  prices = prices.map(price => {
    let str = price.textContent.trim();
    let ind = str.indexOf("z") - 1;
    str = str.substr(0, ind);
    newStr = "";
    str = str.replace(",", ".");
    for (let i = 0; i < str.length; i++) {
      if ("0123456789.".includes(str[i])) newStr += str[i];
    }
    return parseFloat(newStr);
  });
  amountsOfRam = amountsOfRam.map(ram => {
    let str = ram.textContent;
    let ind = str.indexOf("G") - 1;
    str = str.substr(0, ind);
    return parseInt(str);
  });

  phones = [];
  for (let i = 0; i < names.length; i++) {
    phones.push({
      model: names[i].textContent.trim(),
      price: prices[i],
      amountOfRam: amountsOfRam[i],
      unitPrice: Math.round(prices[i] / amountsOfRam[i] * 100) / 100
    });
  }

  phones.sort((a, b) => a.unitPrice - b.unitPrice);
  for (let i = 1; i <= phones.length; i++) {
    console.log(i + ".\t" + phones[i - 1].model + "\nCena: " + phones[i - 1].price + " zł\nCena na GB RAMu: " + phones[i - 1].unitPrice + " zł\n");
  }
  process.exit(0);
});
