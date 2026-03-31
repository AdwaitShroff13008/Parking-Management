'use client'

import { useState } from 'react'
import { Layers } from 'lucide-react'

type Card = {
  id: number
  imgSrc: string
  title: string
}

export default function FloatingCards() {
  const [activeCard, setActiveCard] = useState<number | null>(null)

  const cards: Card[] = [
    { id: 1, imgSrc: 'https://images.unsplash.com/photo-1541888086425-d81bb19240f5?auto=format&fit=crop&w=800&q=80', title: 'Level 5 (Roof)' },
    { id: 2, imgSrc: 'https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?auto=format&fit=crop&w=800&q=80', title: 'Level 4' },
    { id: 3, imgSrc: 'https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=800&q=80', title: 'Level 3' },
    { id: 4, imgSrc: 'https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=800&q=80', title: 'Level 2' },
    { id: 5, imgSrc: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80', title: 'Level 1' },
    { id: 6, imgSrc: 'https://images.unsplash.com/photo-1629853928424-df35eb270034?auto=format&fit=crop&w=800&q=80', title: 'Ground Level' },
  ]

  const handleCardClick = (id: number) => {
    setActiveCard(activeCard === id ? null : id)
  }

  return (
    <div className="relative w-full h-screen bg-neutral-900 flex items-center justify-center overflow-hidden">
      {/* Container with isometric perspective */}
      <div 
        className="relative w-80 h-80"
        style={{
          transformStyle: 'preserve-3d',
          transform: 'rotateX(60deg) rotateZ(-45deg)',
        }}
      >
        {cards.map((card, index) => {
          const isClicked = activeCard === card.id
          
          // Cards are stacked sequentially on the Z axis (which visually points up due to rotateX)
          // Lower index = higher floor = higher Z value.
          const zOffset = (cards.length - 1 - index) * 60 
          
          return (
            <div
              key={card.id}
              onClick={() => handleCardClick(card.id)}
              className="absolute inset-0 w-full h-full rounded-xl transition-all duration-500 ease-out cursor-pointer group"
              style={{
                // Base transformation for the floor's level in the stack
                // When clicked, extract X and Y fully
                transform: `
                  translateZ(${zOffset}px) 
                  ${isClicked ? 'translateX(120px) translateY(-120px)' : ''}
                `,
              }}
            >
              {/* Inner wrapper for hover transform inside the Z-plane */}
              <div 
                className="w-full h-full relative rounded-xl overflow-hidden border-2 border-white/20 bg-neutral-800 transition-transform duration-300 group-hover:-translate-x-4 group-hover:-translate-y-4 shadow-[5px_5px_15px_rgba(0,0,0,0.5)] group-hover:shadow-[15px_15px_25px_rgba(0,0,0,0.6)]"
              >
                <img 
                  src={card.imgSrc} 
                  alt={card.title}
                  className="w-full h-full object-cover opacity-70 group-hover:opacity-100 transition-opacity"
                  loading="lazy"
                />
                <div className="absolute right-4 bottom-4 bg-black/60 text-white px-3 py-1.5 rounded-full text-sm font-medium flex items-center justify-center gap-2 backdrop-blur-sm group-hover:bg-blue-600/80 transition-colors">
                  <Layers className="w-4 h-4" />
                  {card.title}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
