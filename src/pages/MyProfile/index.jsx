import jsCookies from 'js-cookies';
import React, { useContext, useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import Profile from '../../components/Profile';
import authorService from '../../services/author';
import { UserContext } from '../../UserContext';
import './styles.css';
const MyProfile = () => {
  const { user, setUser } = useContext(UserContext);
  const [displayName, setDisplayName] = useState(user.author.displayName);
  const [profileImage, setProfileImage] = useState(user.author.profileImage);
  const [editProfile, setEditProfile] = useState(false);
  const [github, setGithub] = useState(user.author.github);
  const history = useHistory();
  const handleProfileChange = async (event) => {
    try {
      // get self object
      const response = await authorService.getAuthor(user.author.authorID);
      const author_data = response.data;
      author_data.displayName = displayName;
      author_data.profileImage = profileImage;
      author_data.github = github;


      console.log(
        await authorService.updateAuthor(
          jsCookies.getItem('csrftoken'),
          user.author.authorID,
          author_data
        )
      );
      setDisplayName(displayName);
      setProfileImage(profileImage);
      setGithub(github);
      setUser({
        ...user, author: {
          ...user.author,
          displayName: displayName,
          profileImage: profileImage,
          github: github
        }});

    } catch (e) {
      alert('Error updating profile.');
      setDisplayName('');
      setProfileImage('');
      setGithub('');
    }
  };

  // redirect to home if not logged in
  useEffect(() => {
    if (user.author.authorID === null) {
      history.push('/');
    }
  });

  return (
    <div className='profileContainer'>
      <Profile author={user.author} buttonText={"Edit"} onClick={() => {setEditProfile(!editProfile)}} />
      { editProfile && 
        <div className='updateProfileContainer'>
          <label>
            <div>New Display Name</div>
            <input
              type='text'
              onChange={(e) => setDisplayName(e.target.value)}
              defaultValue={user.author.displayName}
            ></input>
          </label>
          <br />
          <label>
            <div>New Profile Image Link</div>
            <input
              type='text'
              onChange={(e) => {
                setProfileImage(e.target.value);
              }}
              defaultValue={user.author.profileImage}
            ></input>
          </label>
          <br />
          <label>
            <div>New Gitub Link</div>
            <input
              type='text'
              onChange={(e) => setGithub(e.target.value)}
              defaultValue={user.author.github}
            ></input>
          </label>
          <br />
          <button className="submitButton" onClick={handleProfileChange}>SUBMIT</button>
        </div>
      }
    </div>
  );
};

export default MyProfile;
