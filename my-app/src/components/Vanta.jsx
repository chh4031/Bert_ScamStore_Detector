import React, { useRef, useEffect } from "react";
import * as THREE from "three";
// import NET from "../../node_modules/vanta/dist/vanta.net.min";
// import NET from "../../node_modules/vanta/dist/vanta.net.min";

const Vanta = () => {
  const vantaRef = useRef(null);
  const vantaEffect = useRef(null);

  useEffect(() => {

    let NET;

    import("vanta/dist/vanta.net.min").then((mod) => {NET = mod.default;
        if (!vantaEffect.current && vantaRef.current) {
        vantaEffect.current = NET({
          el: vantaRef.current,
          THREE,
          color: 0xfc9a55,
          backgroundColor: 0xe56204,
          points: 10.0,
          maxDistance: 20.0,
          spacing: 15.0,
          mouseControls: true,
          touchControls: true,
          gyroControls: false,
          vertexColors: true,
        });
    }
});

    // if (!vantaEffect.current && vantaRef.current) {
    //   vantaEffect.current = NET({
    //     el: vantaRef.current,
    //     THREE,
    //     color: 0xfc9a55,
    //     backgroundColor: 0xe56204,
    //     points: 10.0,
    //     maxDistance: 20.0,
    //     spacing: 15.0,
    //     mouseControls: true,
    //     touchControls: true,
    //     gyroControls: false,
    //     vertexColors: true,
    //   });
    // }

    return () => {
      if (vantaEffect.current) vantaEffect.current.destroy();
    };
  }, []);

  return (
    <div
      ref={vantaRef}
      style={{
        width: "100vw",
        height: "100vh",
        overflow: "hidden",
        position: "relative",
      }}
    >
      <div
        style={{
          position: "relative",
          zIndex: 1,
          color: "white",
          textAlign: "center",
          paddingTop: 100,
          userSelect: "none",
        }}
      >
        <h1>Vanta.js NET 효과 테스트</h1>
        <p>이 영역 위에 Vanta.js 배경 효과가 나와야 합니다.</p>
      </div>
    </div>
  );
}

export default Vanta;