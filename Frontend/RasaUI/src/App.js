import './App.css';



import React from "react";
import ReactDOM from "react-dom";
import logo from './/myAI-ggMIaIHkf-transformed.jpeg'
import logoo from './/brainer.png'
import logooo from './/valley.jpg'
import { Routes, Route } from 'react-router';
import Basic from './components/Basic';
import { Mainpage } from './components/Mainpage';
import { Link, NavLink } from 'react-router-dom';

// function App(){
//   return (
//     <>
    
//       <li>
//    <Link to="/main">Valley Chat</Link>
//    </li>
//    <li>
//     <Link to="/components">Chatbot</Link>
//     </li>
    
//   <Routes>
//     <Route path="/main" element = {<Mainpage />} />
//     <Route path="/components" element = {<Basic />} />
  
//   </Routes>
//   </>
//   )
// }

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      images: [
        logo,
        logooo,
        logoo
      ],
      selectedImage: logo
    };
  }

  componentDidMount() {
    let intervalId = setInterval(() => {
      this.setState(prevState => {
        if (prevState.selectedImage === this.state.images[0]) {
          return {
            selectedImage: this.state.images[1]
          };
        } else if (prevState.selectedImage === this.state.images[2]){
          return {
            selectedImage: this.state.images[0]
          };
        }
        else if (prevState.selectedImage === this.state.images[1]){
          return {
            selectedImage: this.state.images[2]
          };
        }
      });
    }, 10000);

    this.setState({
      intervalId
    });
  }

  componentWillUnmount() {
    clearInterval(this.state.intervalId);
  }
 

  render() {
    return (
      
      <div className="App">
    
      <Routes>
            <Route path="/main" element = {<Mainpage />} />

      </Routes>
     
    <img src={this.state.selectedImage} style={{width: '100%',
    height: '800px',
    position:'absolute',
    left:0,
    backgroundImage: `url(${this.state.selectedImage})`,
    backgroundSize: 'cover'  }}/>

      
    
      <li>
      
    
    <NavLink style={({ isActive }) =>
              isActive
                ? {
                    color: '#fff',
                    background: '#7600dc',
                    position:'absolute',
                    display:"inline-block",
                    border: "10px solid rgb(118, 0, 220)",
                    textAlign: "left",
                    left:7
                 
                  }
                : { color: '#fff', background: '#7600dc',position:'absolute',display:"inline-block", border: "10px solid rgb(118, 0, 220)", textAlign: "left",left:7}
            }
  
   to="/main">
      Home
      </NavLink>
    </li>
    
  <Routes>
    
    <Route path="/components" element = {<Basic />} />
  
  </Routes>
  
     
        
         
        
        
        
       
         
      </div>
      
    );
  }
}

export default App;
