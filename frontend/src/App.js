import 'bootstrap/dist/css/bootstrap.min.css'
import Navbar from './components/Navbar/Navbar';
import DynamicTabs from './components/Tabs/DynamicTabs';
import DatabaseTree from './components/DatabaseTree/DatabaseTree';

function App() {
  return (
    <div className="-">
      <header className="App-header">
        <Navbar />
      </header>
      <body>
        <div className='container-fluid'>
          <div className='row'>
            <DatabaseTree />
            <DynamicTabs />
          </div>
        </div>
      </body>
    </div>
  );
}

export default App;