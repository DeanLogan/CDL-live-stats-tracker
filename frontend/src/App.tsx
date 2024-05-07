import { useState, useEffect } from 'react';
import './App.css';
import { RowData, CustomizedTables } from './components/Table/Table';

interface Player {
  name: string;
  kills: number;
  deaths: number;
  kd: number;
}

function createData(
  player: string,
  kill: number,
  death: number,
  kd: number,
): RowData {
  return { player, kill, death, kd };
}

function App() {
  const [rows1, setTableData1] = useState<RowData[]>([]);
  const [rows2, setTableData2] = useState<RowData[]>([]);

  useEffect(() => {
    const data = [
      createData('Player1', 10, 2, 5),
      createData('Player2', 15, 3, 5),
      createData('Player3', 20, 4, 5),
      createData('Player4', 20, 4, 5),
    ];
    setTableData1(data);
    setTableData2(data);
  }, []);

  const [message, setMessage] = useState('');

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8080');
    
    ws.onmessage = function (event) {
      const playerData: RowData[] = [];
      setMessage(JSON.parse(event.data).message);
      JSON.parse(event.data).players.forEach((element: Player) => { 
        console.log(element);
        console.log(element.name);
        playerData.push(createData(element.name, element.kills, element.deaths, element.kd));
      });
      setTableData1(playerData);
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <>
      <h1>CDL Live Stat Tracker</h1>
      <div className="card" id="team1">
        <CustomizedTables rows={rows1}/>
      </div>
      <div className="card" id="team2">
        <CustomizedTables rows={rows2}/>
      </div>
      <div className="server-test">
          <h2>WebSocket Example</h2>
          <p>{message}</p>
      </div>
    </>
  )
}

export default App
