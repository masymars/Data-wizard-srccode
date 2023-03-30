import React, { useState,useEffect } from 'react';
import './home.css';
import ItemsetsVisualization from './ItemsetsVisualization';
import { SERVER_KEY, SECRET_KEY } from '../keys';
function Home() {
    const [csvData, setCsvData] = useState([]);
    const [headers, setHeaders] = useState([]);
    const [len, setlen] = useState();
    const [autoOption, setAutoOption] = useState('manual');
    const [threshold, setThreshold] = useState(0.5);
    const [showPriorityPopup, setShowPriorityPopup] = useState(false);
    const [priorities, setPriorities] = useState([]);
    const [numOfItems, setNumOfItems] = useState(0);
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [returnedData, setReturnedData] = useState([]);
    const [showGetRules, setShowGetRules] = useState(false);
    const [showRulesPopup, setShowRulesPopup] = useState(false);
    const [confidence, setConfidence] = useState(0.5);
    const [rulesData, setRulesData] = useState([]);

    const handleFileUpload = (e) => {
        setFile(e.target.files[0]);
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (event) => {
        const csvText = event.target.result;
        setlen(csvText.split('\n').length);
        const rows = csvText.split('\n').slice(0, 20);
        const data = rows.map((row) => row.split(','));
        setHeaders(data.shift()); // Remove first row and store as headers
        setCsvData(data);
      };
      reader.readAsText(file);
    };
  

    const onFileUpload = async () => {
        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        formData.append("minsup", threshold); // Send minsup value

        const response = await fetch(SERVER_KEY+'/upload', {
          method: 'POST',
          body: formData,
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            setReturnedData(data);
            setShowGetRules(true);
          
          
        } else {
          alert('Error uploading file');
        }

        setLoading(false);
      };
    const handleAutoOptionChange = (e) => {
      setAutoOption(e.target.value);
    };
  
    const handleThresholdChange = (e) => {
      setThreshold(e.target.value);
    };
  
  
    useEffect(() => {
      setPriorities(Array(headers.length).fill(0));
    }, [headers]);
  
    const handlePriorityChange = (event, index) => {
      const newPriorities = [...priorities];
      newPriorities[index] = parseInt(event.target.value);
      setPriorities(newPriorities);
    };
  
    const isDuplicatePriority = (index) => {
      return priorities.indexOf(priorities[index]) !== index;
    };
    const togglePriorityPopup = () => {
      setShowPriorityPopup(!showPriorityPopup);
    };

/////////////////////////////////////////////////////


const handleSendButtonClick = async() => {
    if (isValidInput()) {
    setShowPriorityPopup(!showPriorityPopup);
  // Implement the logic to send data to the flex server here


  setLoading(true);
  const formData = new FormData();
  formData.append('file', file);
  formData.append("prio", priorities); 

  const response = await fetch(SERVER_KEY+'/get-minsup', {
    method: 'POST',
    body: formData,
  });
  
  if (response.ok) {
      const data = await response.json();
      console.log(data);
      setThreshold(data);
      
    
    
  } else {
    alert('Error uploading file');
  }

  setLoading(false);
  console.log("Sending data to flex server...");

}else {
    alert("Please ensure all priority values are unique and greater than 0.");
  }
};

const isValidInput = () => {
    const uniquePriorities = new Set(priorities.filter(priority => priority > 0));
    return uniquePriorities.size === priorities.length && uniquePriorities.size === headers.length;
  };
const renderPriorityChooser = () => {
    
  
    
  
    if (autoOption === 'auto-gg') {
      return (
        <>
          <button onClick={togglePriorityPopup} class="set-priorities-btn">Set Column Priorities</button>
          <span className="selection-label">Minsup:</span>
            <input
                    id="threshold-input"
                    className="threshold-input"
                    type="number"
                    value={threshold}
                    min={0}
                    max={1}
                    step={0.01}
                    onChange={handleThresholdChange}
                  />
          {showPriorityPopup && (
            <div className="priority-popup">
              <h3>Column Priorities:</h3>
              {headers.map((header, index) => (
                <div key={index} className="options-row">
                  <span className="selection-label">{header}:</span>
                  <input
                    className={`threshold-input ${isDuplicatePriority(index) ? 'duplicate-priority' : ''}`}
                    type="number"
                    min={1}
                    max={headers.length}
                    value={priorities[index]}
                    onChange={(event) => handlePriorityChange(event, index)}
                  />
                </div>
              ))}
              <div class="div-set-priorities-btn">
                <button onClick={togglePriorityPopup} class="set-priorities-btn">Close</button>
                <button onClick={handleSendButtonClick} class="set-priorities-btn">Send</button>
              </div>
            </div>
          )}
        </>
      );
    }
    return null;
  };


    const handleNumOfItemsChange = (e) => {
      setNumOfItems(parseInt(e.target.value));
    };
    
    const predictMinSupport = async () => {
        setShowPriorityPopup(!showPriorityPopup);
  // Implement the logic to send data to the flex server here


  setLoading(true);
  const formData = new FormData();
  formData.append('file', file);
  formData.append("numitems", numOfItems); 

  const response = await fetch(SERVER_KEY+'/predict', {
    method: 'POST',
    body: formData,
  });
  
  if (response.ok) {
      const data = await response.json();
      console.log(data);
      setThreshold(data);
      
    
    
  } else {
    alert('Error uploading file');
  }

  setLoading(false);
  console.log("Sending data to flex server...");
      };
   
    const renderAiOptions = () => {
      if (autoOption === 'auto-ai') {
        return (
          <div className="options-row">
            <span className="selection-label">Nb itemSets:</span>
            <input
              className="threshold-input"
              type="number"
              min={0}
              value={numOfItems}
              onChange={handleNumOfItemsChange}
            />
            <span className="selection-label">Minsup:</span>
            <input
                    id="threshold-input"
                    className="threshold-input"
                    type="number"
                    value={threshold}
                    min={0}
                    max={1}
                    step={0.01}
                    onChange={handleThresholdChange}
                  />
            <button  class="set-priorities-btn" onClick={predictMinSupport}>
              Predict
            </button>
          </div>
        );
      }
      return null;
    };



    /////////////////////returned value /////////////////////////////
    const renderReturnedData = () => {
        return (
          <div className="itemset-table-container" >
            <div className="rules-heading-container">
            <h2 className='tb_h2'>Itemsets :</h2>
         <span className="num-rules">
      ({returnedData.length} set)
    </span>
    </div>
            
            <div className="itemset-table-incontainer">
            <table className="itemset-table">
              <thead className="fixed-header">
                <tr>
                  <th>Itemset</th>
                  <th>Support</th>
                </tr>
              </thead>
              <tbody>
                {returnedData.map((row, index) => (
                  <tr key={index}>
                    <td>{row.itemset.join(", ")}</td>
                    <td>{row.support.toFixed(4)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            </div></div>
        );
      };

 ///////render value //////
     
 const renderRulesTable = () => {
     
    return (
      <div className="cont-bb rules-table-container  ">
        <div className="rules-heading-container">
         <h2 className='tb_h2'>Rulles</h2>
         <span className="num-rules">
      ({rulesData.length} rules)
    </span>
    </div>
        <div className="itemset-table-incontainer">
       
        <table className="rules-table itemset-table">
          <thead className="fixed-header">
            <tr>
              <th>Antecedents</th>
              <th>Consequents</th>
              <th>Support</th>
              <th>Confidence</th>
              <th>Lift</th>
              <th>Leverage</th>
              <th>Conviction</th>
            </tr>
          </thead>
          <tbody className="rules-table itemset-table">
            {rulesData.map((rule, index) => (
              <tr key={index}>
                <td>{rule.antecedents.join(', ')}</td>
                <td>{rule.consequents.join(', ')}</td>
                <td>{rule.support}</td>
                <td>{rule.confidence}</td>
                <td>{rule.lift}</td>
                <td>{rule.leverage}</td>
                <td>{rule.conviction}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div></div>
    );
  }
  
      /////////////////////////////////////////rulles//////////////////
      const handleGetRulesClick = () => {
        console.log("clicked")
        setShowRulesPopup(true);
      };
      const handleRulesSubmit = async (numRules) => {
    
        setLoading(true);
        setShowRulesPopup(false);
        const response = await fetch(SERVER_KEY+"/get_rules", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ num_rules: numRules,
            confidence: confidence, }),
        });
      
        if (response.ok) {
          // ffffffffffffffff
          const datas = await response.json();
            console.log(datas);
          setRulesData(datas);
            setShowGetRules(true);
         
            
        } else {
          alert("Failed to get rules");
        }
        setLoading(false);
       
      };

      const RulesPopup = ({ onSubmit, onClose }) => {
        const [numRules, setNumRules] = useState(1);
      
        const handleSubmit = () => {
          onSubmit(numRules);
        };
      
    
        return (
            <div className="rules-popup">
            <div className="rules-popup-content">
              <button className="close-button" onClick={onClose}>&times;</button>
              <div className="input-container">
                <label htmlFor="confidence">Number of Rules : </label>
              
              <input
                type="number"
                min="1"
                value={numRules}
                onChange={(e) => setNumRules(parseInt(e.target.value))}
              /></div>
              <div className="input-container">
                <label htmlFor="confidence">Confidence : </label>
                <input
                  id="confidence"
                  type="number"
                  value={confidence}
                  min="0"
                  max="1"
                  step="0.01"
                  onChange={(e) => setConfidence(parseFloat(e.target.value))}
                />
              </div>
              <button onClick={handleSubmit } className="upload-btn">Submit</button>
              
            </div>
          </div>
        );
      };
    return (
        <div className="Home">
                    {loading && <div className="loader"></div>}
                    {showRulesPopup && (
  <RulesPopup onSubmit={handleRulesSubmit} onClose={() => setShowRulesPopup(false)} />
)}
      <div className="container ">
      
        <div class="area" >
              <ul class="circles">
                      <li></li>
                      <li></li>
                      <li></li>
                      <li></li>
                      <li></li>
                      <li></li>
                      <li></li>
                      <li></li>
                      <li></li>
                      <li></li>
              </ul>
      </div >
        <div className="wrapper context">
          <h1>Data Wizard</h1>
          <div className='one_row'>
          <label for='file-upload' class='file-upload-btn'>
    Choose a file
    <input id='file-upload' type='file' onChange={handleFileUpload} />
  </label>
  {file && ( 
  <button className="upload-btn" onClick={onFileUpload}>
          Appriori 
        </button>)}


  <div className='options options-row'>
              <div  className="options-select">
              <span className="selection-label">Minsup Method :  </span>
              <select
                id="auto-select"
                className="custom-select"
                value={autoOption}
                onChange={handleAutoOptionChange}
              >
                  <option value='manual'>Manual</option>
                  <option value='auto-ai'>predect AI</option>
                  <option value='auto-gg'>Adaptive sup</option>
                  
                </select>
              </div>
              {autoOption == 'manual' && (
                <div className='threshold-option'>
                                 <span className="selection-label">Minsup:</span>
                  <input
                    id="threshold-input"
                    className="threshold-input"
                    type="number"
                    value={threshold}
                    min={0}
                    max={1}
                    step={0.01}
                    onChange={handleThresholdChange}
                  />
  
                </div>
              )}
              {csvData.length > 0 && renderPriorityChooser()}
              {csvData.length > 0 && renderAiOptions()}
            </div>
            </div>
            <div className="tables-container">
          <td class='td-f' >
          <p>{`Rows: ${len}   `}</p>
             <p>{`  Columns: ${headers.length}`}</p></td>
          {csvData.length > 0 && (
            <div class="table-container">
            <table className="csv-table">
           
              <thead>
                <tr>
                  {headers.map((header, index) => (
                    <th key={index}>{header}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {csvData.map((row, index) => (
                  <tr key={index}>
                    {row.map((cell, index) => (
                      <td key={index}>{cell}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
            </div>
          )}
          <div className="tables-row">
    {returnedData.length > 0 && renderReturnedData()}
    { returnedData.length  > 0 ? (
    <div className='tree-div'>
            <h2 className='tb_h2'>Visulization :</h2>
    {returnedData.length  < 40  ? (
  <ItemsetsVisualization returnedData={returnedData} />
) : (
    <div className="large-data-message">
    <p>Can't visualize data - too big.</p>
  </div>
)}  </div>) : (<div></div>)}
    </div>
    {showGetRules && (
  <button className="get-rules-btn upload-btn" onClick={handleGetRulesClick}>
    Get Rules
  </button>
)}
    {rulesData.length > 0 &&  renderRulesTable()}
    

    </div>
        </div>
      </div></div>
    );
  }

  export default Home;