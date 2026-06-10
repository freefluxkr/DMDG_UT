import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";

// 사장님이 가져다 주신 Firebase Config
const firebaseConfig = {
  apiKey: "AIzaSyAnISNciX3r53A3oLR4FaLUNpmyKkiharc",
  authDomain: "dmdg-pwa.firebaseapp.com",
  projectId: "dmdg-pwa",
  storageBucket: "dmdg-pwa.firebasestorage.app",
  messagingSenderId: "998738485811",
  appId: "1:998738485811:web:9d49012ec8b1d3c5bf7946",
  measurementId: "G-WZNW6P49VM"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Cloud Firestore and get a reference to the service
export const db = getFirestore(app);

// Initialize Cloud Storage and get a reference to the service
export const storage = getStorage(app);

// Legacy compat exposure
if (typeof window !== "undefined") {
  window.db = db;
}

export default app;
