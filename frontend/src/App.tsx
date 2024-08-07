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

const defaultTeam1Data: RowData[] = [
  createData('Player1', 0, 0, 0),
  createData('Player2', 0, 0, 0),
  createData('Player3', 0, 0, 0),
  createData('Player4', 0, 0, 0),
];

const defaultTeam2Data: RowData[] = [
  createData('Player5', 0, 0, 0),
  createData('Player6', 0, 0, 0),
  createData('Player7', 0, 0, 0),
  createData('Player8', 0, 0, 0),
];

function App() {
  const [rows1, setTableData1] = useState<RowData[]>(defaultTeam1Data);
  const [rows2, setTableData2] = useState<RowData[]>(defaultTeam2Data);
  const [team1Name, setTeam1Name] = useState<string>('Team 1');
  const [team2Name, setTeam2Name] = useState<string>('Team 2');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8080');
    
    ws.onmessage = function (event) {
      console.log(message)
      const data = JSON.parse(event.data);
      setMessage(data.message);

      setTeam1Name(data.team1Name);
      setTeam2Name(data.team2Name);

      const team1Data: RowData[] = data.team1.map((player: Player) => 
        createData(player.name, player.kills, player.deaths, player.kd)
      );

      const team2Data: RowData[] = data.team2.map((player: Player) => 
        createData(player.name, player.kills, player.deaths, player.kd)
      );

      setTableData1(team1Data);
      setTableData2(team2Data);
    };

    return () => {
      ws.close();
    };
  } );

  return (
    <>
      <h1>CDL Live Stat Tracker</h1>
      <div className="card" id="team1">
        <h2>{team1Name}</h2>
        <CustomizedTables rows={rows1}/>
      </div>
      <div className="card" id="team2">
        <h2>{team2Name}</h2>
        <CustomizedTables rows={rows2}/>
      </div>
    </>
  )
}

export default App;