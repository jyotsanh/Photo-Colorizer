import React from 'react';
import './about.css';

const AboutUs = () => {
  return (
    <div className="about-container">
      <header className="about-header">
        <h1 className="about-title">About Us</h1>
      </header>
      <div className="about-content">
        <p>
          Temple vision is a place where the purpose of our project is for people to see the preserved work of past architecture of the city of temple Kathmandu. Our AI powered system decolorifies the image given by the user of Temple in black and white in color which gives the view to the past relic or memory.
        </p>
        <p>
          Purpose of the project is to give the younger generation a memory visit to the past lane of History and to give the older generation a revisit of the memory lane.
        </p>
        <p>
          Interns of scales, our project boundary has been set in Nepal's capital city Kathmandu (City of Temple).
        </p>
      </div>
     
    </div>
  );
};

export default AboutUs;
