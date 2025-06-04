import pg1 from '../assets/pg1.png';
import pg2 from '../assets/pg2.png';
import pg3 from '../assets/pg3.png';
import React, { useRef, useEffect, useState} from "react";
import * as THREE from "three";
import "../styles/Home.css"; // CSS 파일 import
import DountChart from './DountChart';

const Home = () => {
    const vantaRef = useRef(null);
    const vantaEffect = useRef(null);

    const [message, setMessage] = useState("");
    const [response, setResponse] = useState({
      FK_result : '',
      FK_choice : '',
      FK_name : '',
      FK_open : '',
      FK_country : '',
      FK_fake : '',
      FK_sname : ''
    });

    const [showResult, setShowResult] = useState(false);

    const handleClick = async () => {

      const data = {message : message};
      console.log("넘어갈 데이터 테스트", data)

      const res = await fetch("http://localhost:5000/api", {
        method : "POST",
        headers: {
          'Content-Type' : 'application/json',
        },
        body : JSON.stringify(data),
      });
      console.log(res)

      const result = await res.json();

      setResponse({
        FK_result : result.FK_result,
        FK_choice : result.FK_choice,
        FK_name : result.FK_name,
        FK_open : result.FK_open,
        FK_country : result.FK_country,
        FK_fake : result.FK_fake,
        FK_sname : result.FK_sname
      });

      setShowResult(true);
    }


    useEffect(() => {

        // vanta 모듈 못 불러와서 useEffect에서 직접 import 해서 사용함
        let NET;

        import("vanta/dist/vanta.waves.min").then((mod) => {NET = mod.default;
            if(!vantaEffect.current && vantaRef.current){
                vantaEffect.current = NET({
                    el: vantaRef.current,
                    THREE,
                    color: 0xB44D03,
                    shininess: 10.0,
                    waveHeight: 10.0,
                    waveSpeed: 0.4,
                    zoom: 1.0,
                    backgroundColor: 0x000000,
                    mouseControls: true,
                    touchControls: true,
                    gyroControls: false,
                    vertexColors: true,
                });
            }
        });

        return () => {
            if (vantaEffect.current) vantaEffect.current.destroy();
        };
    }, []);

    const textNum = Number(response.FK_result)
    let textDiff = "";

    if (textNum <= 30){
      textDiff = '"해당 제품의 사기 위험도는 낮습니다."'
    }else if (textNum > 30 && textNum < 50){
      textDiff = '"해당 제품의 사기 위험도는 보통입니다."'
    }else if(textNum > 50 && textNum < 80){
      textDiff = '"해당 제품의 사기 위험도는 다소 높습니다."'
    }else{
      textDiff = '"해당 제품의 사기 위험도는 매우 높습니다."'
    }

  return (
    <div className="home">
      <header className="header">
          <div className="logo">
            <a href=''><strong>SC.AI</strong></a>
          </div>
        <nav className="nav">
          <a href="#">사기 스토어란?</a>
          <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>
          <a href="#">사기 스토어 구분</a>
          <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>
          <a href="#">사기 피해 방지</a>
          <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>
          <a href="#">사기 제보</a>
        </nav>
        <div className="auth-buttons">
          <button className="login-btn">로그인</button>
          <button className="signup-btn">회원가입</button>
        </div>
      </header>

      <section className="hero" ref={vantaRef}>
        <p>AI 기반 해외직구 플랫폼 사기 스토어 탐지 시스템</p>
        <h1>클릭 한번이면 쉽게 탐지</h1>
        <p><strong>SC.AI</strong>는 해외 직구 플랫폼에 등록된 제품이 사기인지 판단해주는 <strong>무료서비스</strong>입니다.</p>
        <div className="input-area">
          <input 
          type="text" 
          placeholder="제품 링크를 입력해주세요." 
          value={message}
          onChange={(e) => setMessage(e.target.value)}/>
          <button onClick={handleClick}>사기 탐지하기</button>
        </div>
      </section>
      {showResult ? (
      <section className="result-section">
        <h3>{textDiff}</h3><br/>
        <div className='analysis-section'>
          <div className="analysis-box_left">
            <h2>분석결과</h2><br/>
            <p><strong>플랫폼:</strong> AliExpress</p>
            <p><strong>제품명:</strong> {response.FK_name}</p>
            <p><strong>배송지:</strong> {response.FK_country}</p>
            <p><strong>스토어명:</strong> {response.FK_sname}</p>
            <p><strong>스토어 생성일:</strong> {response.FK_open}</p>
            <p><strong>choice 유무:</strong> {response.FK_choice}</p>
            <p><strong>어색하게 번역된 한국어 리뷰 개수 비율:</strong> {response.FK_fake} 개</p>
            <p><strong>서버 응답(테스트 용 %):</strong> {response.FK_result} %</p>
            <br/><br/><br/>
            <div className='ptxt'>
              <a href=''>자세히 알아보기</a>
            </div>
          </div>
          
          <div className="analysis-box_right">
            <div className="donut-chart">
              <DountChart percentage={response.FK_result}/>
            </div>
            <ul>
              <span style={{ color: "green" }}>30% 이하 : 사기 가능성 낮음</span>
              <span style={{ color: "#CC9900" }}>31% ~ 50% : 사기 가능성 있음</span>
              <span style={{ color: "#D35400" }}>51% ~ 80% : 사기 가능성 높음</span>
              <span style={{ color: "#B44D03" }}>81% 이상 : 사기 가능성 매우 높음</span>
            </ul>
          </div>
          </div>
          <div className='footxt'>
            <br/><br/><br/>
            <span>AI는 가끔 실수를 할 수 있습니다. </span>
          </div>
        </section>
      ) : (

      <section className="feature-section">
        <h2>“SC.AI는 해외 직구 플랫폼에 최적화된 서비스 입니다”</h2>
        <p>SC.AI는 BERT를 기반으로 학습된 데이터를 바탕으로 해당 제품의 가짜 리뷰를 분석합니다.</p>
        <p>또한 각종 사기 수법들을 분석한 통계를 바탕으로 가중치를 계산해 해당 스토어의 사기 여부 백분률로 제공합니다.</p>
        <p>이는 높은 수준의 정확도를 제공합니다.</p>

        <div><br/><br/></div>

        <div className="features">
          <div className="feature-card">
            <div>&nbsp;</div>
            <img src={pg1}/>
            <div>&nbsp;<br/>&nbsp;</div>
            <h3>BERT 기반</h3>
            <div className='size'>
                <p>BERT 기반 문장 분석을 통해 학습된 리뷰와 번역된 가짜 리뷰의 패턴을 분석합니다.</p>
            </div>
          </div>
          <div className="feature-card">
            <div>&nbsp;</div>
            <img src={pg2}/>
            <div>&nbsp;<br/>&nbsp;</div>
            <h3>통계분석</h3>
            <div className='size'>
                <p>여러 사기 스토어들의 수법 분석한 통계를 바탕으로 가중치를 계산합니다.</p>
            </div>
          </div>
          <div className="feature-card">
            <div>&nbsp;</div>
            <img src={pg3}/>
            <div>&nbsp;<br/>&nbsp;</div>
            <h3>높은 정확도</h3>
            <div className='size'>
                <p>BERT와 통계분석의 양질의 데이터를 사용하여 높은 수준의 정확도를 제공합니다.</p>
            </div>
          </div>
        </div>
      </section>
      )}


      <footer className="footer">
        <p>(주)동서대학교 &nbsp;&nbsp; | &nbsp;&nbsp; 대표자: 조현호 &nbsp;&nbsp; | &nbsp;&nbsp; 사업자등록번호: 20191598</p>
        <p>주소: 부산광역시 사상구 주례동 &nbsp;&nbsp; | &nbsp;&nbsp; 이메일: 20191598@office.dongseo.ac.kr</p>
        <p>본 사이트 운영팀: (주) 동서대학교 &nbsp;&nbsp; | &nbsp;&nbsp; 개인정보처리방침</p>
        <p>COPYRIGHT (주)동서대학교 ALL RIGHTS RESERVED.</p>
      </footer>
    </div>
  );
};

export default Home;