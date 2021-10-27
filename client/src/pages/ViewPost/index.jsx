import React, { useContext, useEffect, useState } from "react";
import { useParams } from "react-router";
import Post from "../../components/Post";
import Comment from "../../components/Comment";
import postService from "../../services/post";
import jsCookies from "js-cookies";
import { Parser, HtmlRenderer } from "commonmark";
import "./styles.css"
import authorService from "../../services/author";
import { UserContext } from "../../UserContext";
import Error from "../Error";

const ViewPost = () => {
  const CMParser = new Parser({ safe: true });
  const CMWriter = new HtmlRenderer();
  const { authorID, postID } = useParams();
  const [ comments, setComments ] = useState([]);
  const [ comment, setComment ] = useState("");
  const [ commentType, setCommentType ] = useState("Text")
  const { user } = useContext(UserContext);
  const [ post, setPost ] = useState([]);

  useEffect(() => {
    const getPost = async () => {
      const response = await postService.getPost(jsCookies.getItem("csrftoken") , authorID, postID);
      const likeRes = await postService.getLikes(authorID, postID);
      setPost({ ...response.data, likes: likeRes.data.items });
    };

    const getComments = async () => {
      const response = await postService.getComments(jsCookies.getItem("csrftoken"), authorID, postID, 1, 5);
      console.log(response)
      setComments(response.data.comments);
    };  

    getPost();
    getComments();
  }, [ authorID, postID ]);

  const submitComment = async () => {
    const authorResponse = await authorService.getAuthor(user.author.authorID);
    console.log(authorResponse)
    const response = await postService.createComment(jsCookies.getItem("csrftoken"), authorID, postID, { contentType: commentType, comment, author: authorResponse.data });
    console.log(response);
    setComments([ { author: authorResponse.data, comment, contentType: commentType }, ...comments ]) 
  };

  return (
    <div>
      { post?.author ? <>
      <div className="myPostContainer">
        <Post post={post} setPost={setPost} />
      </div>
      <div className="myPostContainer">
        { comments && comments.map((comment) => <Comment key={comment.id} id={comment.id} comment={comment} />)}
        <br/>

        <select onChange={(e) => setCommentType(e.target.value === "Text" ? "text/plain" : "text/markdown")}>
          <option>Text</option>
          <option>Markdown</option>
        </select>
        <input onChange={(e) => setComment(e.target.value) } />
        <div>
          <p>Preview</p>
          { commentType === "text/plain" ? 
              <div className='cmPreview'>{comment}</div> 
            :
              <div
                className='cmPreview'
                dangerouslySetInnerHTML={{
                  __html: CMWriter.render(CMParser.parse(comment)),
                }}
              ></div>
          }
        </div>
        <br/>
        <button onClick={submitComment}>Submit Comment</button>
      </div></>
      : <Error />
      }
    </div>  
  );
}

export default ViewPost;