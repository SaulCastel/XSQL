import { useRef, useState } from 'react';
import Navbar from './components/Navbar/Navbar';
import DynamicTabs from './components/Tabs/DynamicTabs';
import DatabaseTree from './components/DatabaseTree/DatabaseTree';
import 'bootstrap/dist/css/bootstrap.min.css'

function App() {
  const dynamicTabsRef = useRef(); // Crear una referencia para DynamicTabs
  const [sqlContent, setSqlContent] = useState({});

  // Acceder a la función addTab a través de la referencia
  const handleNewQuery = () => {
    dynamicTabsRef.current.addTab();
  };

  // Acceder a la función handleExecuteQuery2 a través de la referencia
  const handleExecuteQuery = () => {
    dynamicTabsRef.current.handleExecuteQuery2();
  };

  const handleSaveAsClick = () => {
    dynamicTabsRef.current.handleSaveAsClick();
  };

  const handleToggleEditor = () => {
    dynamicTabsRef.current.handleToggleEditor();
  };

  const dataQuery = (data) => {
    setSqlContent((prevContent) => {
      const key = `query${Object.keys(prevContent).length + 1}`;
      return { ...prevContent, [key]: data };
    });
  };

  return (
    <div className="-" >
      <header className="App-header">
        <Navbar onNewQuery={handleNewQuery} onDataQuery={dataQuery} onExecuteQuery={handleExecuteQuery} handleSaveAsClick={handleSaveAsClick} handleToggleEditor={handleToggleEditor} />
      </header>
      <body >
        <div className='container-fluid'>
          <div className='row'>
            <DatabaseTree />
            <DynamicTabs ref={dynamicTabsRef} sqlContent={sqlContent} />
          </div>
        </div>
      </body>
    </div>
  );
}

export default App;