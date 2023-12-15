import { useRef } from 'react';
import Navbar from './components/Navbar/Navbar';
import DynamicTabs from './components/Tabs/DynamicTabs';
import DatabaseTree from './components/DatabaseTree/DatabaseTree';
import 'bootstrap/dist/css/bootstrap.min.css'

function App() {
  const dynamicTabsRef = useRef(); // Crear una referencia para DynamicTabs

  const handleNewQuery = () => {
    // Acceder a la función addTab a través de la referencia
    dynamicTabsRef.current.addTab();
  };
  
  const handleExecuteQuery = () => {
    // Acceder a la función handleExecuteQuery2 a través de la referencia
    dynamicTabsRef.current.handleExecuteQuery2();
  };

  return (
    <div className="-" >
      <header className="App-header">
        <Navbar onNewQuery={handleNewQuery}/>
      </header>
      <body >
        <div className='container-fluid'>
          <div className='row'>
            <DatabaseTree />
            <DynamicTabs ref={dynamicTabsRef} onExecuteQuery={handleExecuteQuery}/>
          </div>
        </div>
      </body>
    </div>
  );
}

export default App;