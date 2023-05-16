import React from "react";
import video from '../assets/valleychat.mp4'
import music from '../assets/myaudio.mp3'
import { Link, NavLink } from 'react-router-dom';
import { Routes, Route } from 'react-router';
import App from "../App";
import Basic from "./Basic";
import ReactAudioPlayer from 'react-audio-player';

export function Mainpage() {
    return (
        <div className="main">
            <div className="overlay"></div>
            <video src={video} autoPlay loop muted/>
            
            <div className="content">
                <NavLink style={({ isActive }) =>
              isActive
                ? {
                    color: '#64ec0a', textDecoration: "none"
                  }
                : { color: '#64ec0a', textDecoration: "none"}
            }
                to="/components">Welcome to Valley Chat</NavLink>
            </div>
            <ReactAudioPlayer
            src={music}
            autoPlay
            controls
            />
            <Routes>
            <Route path="/components" element = {<Basic />} />
      
            
        
        </Routes>
        
        </div>
    )
}

