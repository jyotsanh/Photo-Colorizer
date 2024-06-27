import ConditionalRoute from "./routes/conditionalRouting";
import { Routes, Route } from "react-router-dom";
import NavBar from "./components/navbar/navbar.jsx";
import Footer from "./components/footer/footer.jsx";


function App(){
  return (
    <>
      <NavBar />
      <Routes>
        <Route path='/*' element={<ConditionalRoute />} />
      </Routes>
      <Footer/>
    </>
  );
};

export default App;
