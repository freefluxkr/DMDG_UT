import React from 'react';

function PaperCutBackground() {
  return (
    <div className="paper-cut-layer">
      {/* Top Layers */}
      <svg className="svg-wave svg-wave-top" style={{ animationDelay: '-2s', zIndex: 3 }} viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg">
          <path fill="#172554" fillOpacity="1" d="M0,64L48,80C96,96,192,128,288,122.7C384,117,480,75,576,69.3C672,64,768,96,864,112C960,128,1056,128,1152,112C1248,96,1344,64,1392,48L1440,32L1440,0L1392,0C1344,0,1248,0,1152,0C1056,0,960,0,864,0C768,0,672,0,576,0C480,0,384,0,288,0C192,0,96,0,48,0L0,0Z"></path>
      </svg>
      <svg className="svg-wave svg-wave-top" style={{ animationDelay: '-5s', zIndex: 2 }} viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg">
          <path fill="#0d9488" fillOpacity="1" d="M0,128L48,138.7C96,149,192,171,288,154.7C384,139,480,85,576,80C672,75,768,117,864,144C960,171,1056,181,1152,165.3C1248,149,1344,96,1392,69.3L1440,43L1440,0L1392,0C1344,0,1248,0,1152,0C1056,0,960,0,864,0C768,0,672,0,576,0C480,0,384,0,288,0C192,0,96,0,48,0L0,0Z"></path>
      </svg>
      <svg className="svg-wave svg-wave-top" style={{ animationDelay: '-8s', zIndex: 1 }} viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg">
          <path fill="#ea580c" fillOpacity="1" d="M0,192L48,181.3C96,171,192,149,288,149.3C384,149,480,171,576,197.3C672,224,768,256,864,240C960,224,1056,160,1152,122.7C1248,85,1344,75,1392,69.3L1440,64L1440,0L1392,0C1344,0,1248,0,1152,0C1056,0,960,0,864,0C768,0,672,0,576,0C480,0,384,0,288,0C192,0,96,0,48,0L0,0Z"></path>
      </svg>

      {/* Bottom Layers */}
      <svg className="svg-wave svg-wave-bottom" style={{ animationDelay: '-1s', zIndex: 3 }} viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg">
          <path fill="#0d9488" fillOpacity="1" d="M0,96L48,112C96,128,192,160,288,165.3C384,171,480,149,576,117.3C672,85,768,43,864,37.3C960,32,1056,64,1152,80C1248,96,1344,96,1392,96L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
      <svg className="svg-wave svg-wave-bottom" style={{ animationDelay: '-4s', zIndex: 2 }} viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg">
          <path fill="#eab308" fillOpacity="1" d="M0,160L48,154.7C96,149,192,139,288,144C384,149,480,171,576,170.7C672,171,768,149,864,149.3C960,149,1056,171,1152,192C1248,213,1344,235,1392,245.3L1440,256L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
      <svg className="svg-wave svg-wave-bottom" style={{ animationDelay: '-7s', zIndex: 1 }} viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg">
          <path fill="#172554" fillOpacity="1" d="M0,224L48,229.3C96,235,192,245,288,224C384,203,480,149,576,133.3C672,117,768,139,864,154.7C960,171,1056,181,1152,192C1248,203,1344,213,1392,218.7L1440,224L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
    </div>
  );
}

export default PaperCutBackground;
