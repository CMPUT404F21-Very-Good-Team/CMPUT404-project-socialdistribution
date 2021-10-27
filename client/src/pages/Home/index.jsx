import Like from "../../components/Like";
import Follow from "../../components/Follow";
import { UserContext } from "../../UserContext";
import { useContext } from "react";
import authorService from "../../services/author";
import jsCookies from "js-cookies";
import './styles.css'
import PostPreview from "../../components/PostPreview";

const Home = ({ inbox, setInbox, followers }) => {
  const { user } = useContext(UserContext);

  const clearInbox = async () => {
    try {
      const response = await authorService.clearInbox(jsCookies.getItem("csrftoken"), user.author.authorID);
      console.log(response)
      setInbox([])
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <div>
      <br></br>
      <div className="mainContainer">
      { inbox && inbox.map((item) => {
        console.log(item);
        if (item.type === "post") {
          return <PostPreview key={item.id} post={item} />
        } else if (item.type.toLowerCase() === "follow") {
          return <Follow key={`${item.actor.id};${item.object.id}`} follow={item} followers={followers} />
        } else if (item.type.toLowerCase() === "like") {
          return <Like key={`${item.object};${item.author.id}`} like={item} />
        } else {
         return <></>
        }
      })}
      <button onClick={clearInbox}>Clear Inbox</button>
      </div>
    </div>
  );
}

export default Home;