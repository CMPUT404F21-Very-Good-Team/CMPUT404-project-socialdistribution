import { HtmlRenderer, Parser } from "commonmark";
import React, { useState } from "react";

const PostEdit = ({ onSubmit, post, hideCheckboxes }) => {
  const getPostType = (type) => {
    if (type === "text/plain") return "Text";
    if (type === "text/markdown") return "Markdown";
    return "File";
  }

  const [title, setTitle] = useState(post.title ? post.title : "");
  const [description, setDescription] = useState(post.description ? post.description : "");
  const [postType, setPostType] = useState(post.contentType ? getPostType(post.contentType) : "Text");
  const [contentType, setContentType] = useState(post.contentType ? post.contentType : "text/plain");
  const [content, setContent] = useState(post.content ? post.content : "");
  const [categories, setCategories] = useState(post.categories ? post.categories.join(", ") : []);
  const [visibility, setVisibility] = useState(post.visibility ? post.visibility : "PUBLIC");
  const [unlisted, setUnlisted] = useState(post.unlisted ? post.unlisted : false);
  const CMParser = new Parser({ safe: true });
  const CMWriter = new HtmlRenderer();

  const parseVisibility = (friendsOnly) => {
    if (friendsOnly) return 'FRIENDS';
    return 'PUBLIC';
  };

  const isEmptyString = (str) => {
    return str.length === 0 || str.trim().length === 0 ? true : false;
  };

  const submitPost = async () => {
    if (isEmptyString(title)) {
      alert('Title cannot be empty.');
      return;
    }
    if (isEmptyString(description)) {
      alert('Description cannot be empty.');
      return;
    }
    if (isEmptyString(postType)) {
      alert('Please choose a content type.');
      return;
    }
    if (isEmptyString(content)) {
      alert('Post content cannot be empty');
      return;
    }

    const now = new Date();

    const postData = {
      type: 'post',
      title: title,
      id: null,
      source: null,
      origin: null,
      description: description,
      contentType: contentType,
      content: content,
      author: null,
      categories: categories.split(","),
      count: 0,
      comments: null,
      published: post.published ? post.published : now.toISOString(),
      visibility: visibility,
      unlisted: unlisted,
    };

    onSubmit(postData);
  };

  const handleFile = (file) => {
    const fileReader = new FileReader();
    fileReader.addEventListener('load', (event) => {
      let dataType = event.target.result.split(',')[0].split(':')[1];
      if (dataType !== 'image/png;base64' && dataType !== 'image/jpeg;base64') {
        dataType = 'application/base64';
      }
      setContent(event.target.result);
      setContentType(dataType);
    });

    if (file) {
      fileReader.readAsDataURL(file);
    } else {
      setContent('');
    }
  };

  const renderContentInput = (type) => {
    if (type === 'Text') {
      return (
        <div className='textContentInput'>
          <div className="header">Content</div>
          <textarea
            onChange={(e) => {
              setContent(e.target.value);
              setContentType('text/plain');
            }}
            value={content}
          />
        </div>
      );
    } else if (type === 'Markdown') {
      return (
        <div>
          <div className='textContentInput'>
            <div className="header">Content</div>
            <textarea
              onChange={(e) => {
                setContent(e.target.value);
                setContentType('text/markdown');
              }}
              value={content}
            />
          </div>
          <div>
            <div className='header'>Preview</div>
            <div
              className='cmPreview'
              dangerouslySetInnerHTML={{
                __html: CMWriter.render(CMParser.parse(content)),
              }}
            ></div>
          </div>
        </div>
      );
    } else if (type === 'File') {
      return (
        <div>
          <br />
          <input
            type='file'
            onChange={(e) => {
              handleFile(e.target.files[0]);
            }}
          ></input>
          <br />
          <br />
          {contentType?.includes('image') ? <img className="previewPic" alt='content_img' src={content} /> : <></>}
        </div>
      );
    }
  };

  return (
    <div>
      <div>
        <div className="header">Title</div>
        <input onChange={(e) => setTitle(e.target.value)} value={title} />
      </div>
      <div>
        <div className="header">Description</div>
        <input onChange={(e) => setDescription(e.target.value)} value={description} />
      </div>
      <br/>
      <select onChange={(e) => setPostType(e.target.value)} value={postType}>
        <option>Text</option>
        <option>Markdown</option>
        <option>File</option>
      </select>
      <div>{renderContentInput(postType)}</div>
      <div>
        <div className="header">Categories</div>
        <input
          onChange={(e) => setCategories(e.target.value)}
          value={categories}
        />
      </div>
      { !hideCheckboxes &&
        <>
        <input
          type='checkbox'
          onChange={(e) => setVisibility(parseVisibility(e.target.checked))}
          checked={visibility === "PUBLIC" ? false : true}
        />
        <label>Friends-Only</label>
        <br />
        <div className='horizontalDiv'></div>
        <input
          type='checkbox'
          onChange={(e) => {setUnlisted(!unlisted);}}
          checked={unlisted}
        />
        <label>Unlisted</label>
        <br />
        </>
      } 
      <button className="submitButton" style={{width: "40%"}} onClick={submitPost}>SUBMIT</button>
    </div>
  );
};

export default PostEdit;