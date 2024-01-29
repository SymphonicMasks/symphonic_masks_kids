import logo from './logo.svg';
import './App.css';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Layout from "./shared/Layout";
import MusicComponent from "./MusicComponent";

function App() {
  return (
      <div>
      <h1>Your Music App</h1>
    <MusicComponent/>
    </div>

  );
}

export default App;
