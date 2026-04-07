import React from 'react';
import { QrCode, Smartphone, Wrench, Megaphone, CreditCard, ArrowRight, CheckCircle, AlertTriangle, BatteryCharging } from 'lucide-react';

const App = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4 font-sans text-gray-800 flex justify-center">
      {/* A4 Paper Container */}
      <div className="bg-white w-full max-w-[210mm] shadow-2xl overflow-hidden relative">
        
        {/* Header / Hero Section */}
        <header className="bg-emerald-700 text-white p-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 opacity-10 transform translate-x-10 -translate-y-10">
            <QrCode size={400} />
          </div>
          
          <div className="relative z-10">
            <p className="text-emerald-200 font-bold tracking-widest text-sm mb-2">次世代ゴルフボール貸出機決済システム</p>
            <h1 className="text-5xl font-extrabold mb-4 tracking-tight">
              QRプリカ
              <span className="text-2xl font-light ml-4 opacity-90">QR Prica System</span>
            </h1>
            <p className="text-xl font-medium max-w-lg leading-relaxed">
              磁気カードのトラブル・保守終了の不安を一掃。<br/>
              「かざすだけ」で始まる、スマートな練習場運営へ。
            </p>
          </div>
        </header>

        {/* The Problem (Current Market Context) */}
        <section className="bg-gray-50 p-6 border-b border-gray-200">
          <div className="flex items-start gap-4">
            <div className="bg-yellow-100 p-3 rounded-full text-yellow-700 mt-1 flex-shrink-0">
              <AlertTriangle size={24} />
            </div>
            <div>
              <h2 className="text-lg font-bold text-gray-700 mb-2">
                磁気カードリーダーの保守・維持にお困りではありませんか？
              </h2>
              <p className="text-sm text-gray-600 leading-relaxed">
                磁気PETカード市場の縮小に伴い、従来のカードリーダーやサプライ品の入手が困難になっています。「QRプリカ」は、これらの課題を解決し、将来にわたって安心して利用できる代替ソリューションです。
              </p>
            </div>
          </div>
        </section>

        {/* Main Features Grid */}
        <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* Feature 1: Maintenance Free */}
          <div className="flex flex-col">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-emerald-100 p-2 rounded-lg text-emerald-700">
                <Wrench size={24} />
              </div>
              <h3 className="text-xl font-bold text-emerald-800">故障知らず・低コスト</h3>
            </div>
            <p className="text-sm text-gray-600 leading-relaxed mb-2">
              完全非接触タイプのため、従来の磁気ヘッド摩耗や詰まりによる故障がゼロに。高価なリーダー交換費用やメンテナンスコストを大幅に削減します。
            </p>
            <ul className="text-xs text-gray-500 space-y-1 pl-2 border-l-2 border-emerald-200">
              <li>• 読取装置にかざすだけでボール排出</li>
              <li>• 物理的な接触がないため長寿命</li>
            </ul>
          </div>

          {/* Feature 2: User Convenience */}
          <div className="flex flex-col">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-blue-100 p-2 rounded-lg text-blue-700">
                <Smartphone size={24} />
              </div>
              <h3 className="text-xl font-bold text-blue-800">スマホで残高確認</h3>
            </div>
            <p className="text-sm text-gray-600 leading-relaxed mb-2">
              QRコードを読み取ることで、利用者はいつでもスマホから「現在のカード残高（金額・カゴ数）」を確認可能。利便性が向上し、フロントへの問い合わせも減少します。
            </p>
            <ul className="text-xs text-gray-500 space-y-1 pl-2 border-l-2 border-blue-200">
              <li>• アプリインストール不要のWeb確認</li>
              <li>• リアルタイムで残高更新</li>
            </ul>
          </div>

          {/* Feature 3: Marketing */}
          <div className="flex flex-col">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-purple-100 p-2 rounded-lg text-purple-700">
                <Megaphone size={24} />
              </div>
              <h3 className="text-xl font-bold text-purple-800">新たな情報発信チャネル</h3>
            </div>
            <p className="text-sm text-gray-600 leading-relaxed">
              残高確認画面は、お客様との貴重な接点です。イベント告知やキャンペーン情報など、BtoCの情報発信スペースとして活用できます。
            </p>
          </div>

          {/* Feature 4: Versatility */}
          <div className="flex flex-col">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-orange-100 p-2 rounded-lg text-orange-700">
                <CreditCard size={24} />
              </div>
              <h3 className="text-xl font-bold text-orange-800">多様な運用スタイル</h3>
            </div>
            <p className="text-sm text-gray-600 leading-relaxed">
              従来の「カード型」に加え、「ラベルシール型」も採用可能。在庫管理の手間をなくし、お客様のネームタグに貼るなど自由な運用が可能です。
            </p>
          </div>
        </div>

        {/* Product Lineup / Usage Image Area */}
        <section className="bg-gray-100 py-6 px-8 mx-4 rounded-xl mb-6">
          <h3 className="text-center font-bold text-gray-700 mb-4 text-lg">選べる2つのスタイルと柔軟な設定</h3>
          
          <div className="flex flex-col md:flex-row gap-6 justify-center items-stretch">
            {/* Style A */}
            <div className="bg-white p-4 rounded-lg shadow-sm flex-1 border border-gray-200 text-center">
              <div className="h-24 bg-gray-200 rounded mb-3 flex items-center justify-center text-gray-400">
                 [PETカード画像]
              </div>
              <h4 className="font-bold text-emerald-700 mb-1">PETカードタイプ</h4>
              <p className="text-xs text-gray-500 text-left">
                従来のプリペイドカードと同じ感覚で利用可能。既存顧客のスムーズな移行に最適です。
              </p>
            </div>

            {/* Style B */}
            <div className="bg-white p-4 rounded-lg shadow-sm flex-1 border border-gray-200 text-center">
               <div className="h-24 bg-gray-200 rounded mb-3 flex items-center justify-center text-gray-400">
                 [QRラベルシール画像]
              </div>
              <h4 className="font-bold text-orange-700 mb-1">ラベルシールタイプ</h4>
              <p className="text-xs text-gray-500 text-left">
                在庫管理不要。お客様の会員証やスマホ、ネームタグに貼付可能。オリジナル台紙での提供も。
              </p>
            </div>
          </div>
          
          {/* Setting Options */}
          <div className="mt-4 pt-4 border-t border-gray-300 flex items-center justify-center gap-6">
            <span className="text-xs font-bold bg-gray-600 text-white px-2 py-1 rounded">設定可能</span>
            <div className="flex items-center gap-2 text-sm font-medium text-gray-700">
              <BatteryCharging size={18} className="text-emerald-600"/>
              金額設定 (円)
            </div>
            <span className="text-gray-400">/</span>
             <div className="flex items-center gap-2 text-sm font-medium text-gray-700">
              <CheckCircle size={18} className="text-emerald-600"/>
              ボールカゴ数設定
            </div>
          </div>
        </section>

        {/* Footer / CTA */}
        <footer className="bg-emerald-900 text-white p-8 mt-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div>
              <h4 className="text-xl font-bold mb-2">導入のご相談・デモのご依頼</h4>
              <p className="text-emerald-200 text-sm">既存設備への適合性など、お気軽にお問い合わせください。</p>
            </div>
            <div className="bg-white text-emerald-900 py-3 px-8 rounded-lg font-bold text-lg shadow-lg flex items-center gap-2">
              <span>03-XXXX-XXXX</span>
              <span className="text-xs font-normal bg-emerald-100 px-2 py-1 rounded ml-2">担当：営業部</span>
            </div>
          </div>
          <div className="mt-6 pt-4 border-t border-emerald-800 text-center text-xs text-emerald-400">
            © QR Prica System. All Rights Reserved.
          </div>
        </footer>

      </div>
    </div>
  );
};

export default App;