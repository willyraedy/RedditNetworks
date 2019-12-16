import snoowrap from 'snoowrap';
import axios from 'axios'
import fs from 'fs';
import path from 'path';

// Alternatively, just pass in a username and password for script-type apps.
const otherRequester = new snoowrap({
  userAgent: 'script:melis-thesis:v0.0.1',
  clientId: 'f_wJd_CV9WBtxg',
  clientSecret: '23iMmeQKcovVMizPwx_5Nn4cg5M',
  username: 'wilburRay',
  password: 'n4JDYt34xJakggnMQD2d7kxw'
});

// That's the entire setup process, now you can just make requests.

// Submitting a link to a subreddit
// .map(post => post.title).then(console.log);

const wait = async (millesconds) => {
  return new Promise((resolve, reject) => {
    setTimeout(resolve, millesconds);
  })
}


const main = async () => {
  const { data } = await axios.get('https://www.reddit.com/reddits.json?limit=100')
  let after = data.data.after;
  let numberOfNewReddits = data.data.children.length;
  let reddits = data.data.children;

  while (numberOfNewReddits > 0) {
    await wait(1000)
    const { data: newData } = await axios.get(`https://www.reddit.com/reddits.json?limit=100&after=${after}`)
    numberOfNewReddits = newData.data.children.length
    reddits = [...reddits, ...newData.data.children]
    after = newData.data.after;
    console.log(`Just added ${numberOfNewReddits}`)
    console.log(`On id: ${after}`)
    console.log(`total: ${reddits.length}`)
  }
  return reddits;
}

main().then((reddits) => {
  console.log(`There are ${reddits.length} subreddits`)
  fs.writeFileSync(path.join(__dirname, './', 'allReddits.json'), JSON.stringify(reddits))
}).catch(console.error)
