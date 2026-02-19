// Image configuration for Credit Gamer Area
// Uses Unsplash Source for free, high-quality images

const SiteImages = {
    // Hero/OG image
    og: 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200&h=630&fit=crop',
    
    // Quiz category images
    quizzes: {
        'credit-basics': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop',
        'credit-cards': 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&h=400&fit=crop',
        'taxes': 'https://images.unsplash.com/photo-1554224154-26032ffc0d07?w=800&h=400&fit=crop',
        'investing': 'https://images.unsplash.com/photo-1611974765270-ca1258634369?w=800&h=400&fit=crop',
        'budgeting': 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=800&h=400&fit=crop',
        'banking': 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&h=400&fit=crop',
        'student-loans': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&h=400&fit=crop',
        'side-hustle': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&h=400&fit=crop',
        'auto': 'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&h=400&fit=crop',
        'insurance': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=400&fit=crop',
        'career': 'https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800&h=400&fit=crop',
        'health': 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&h=400&fit=crop'
    },
    
    // Blog post images
    blog: {
        'credit-building': 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1200&h=600&fit=crop',
        'investing': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=1200&h=600&fit=crop',
        'saving': 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200&h=600&fit=crop',
        'side-hustle': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&h=600&fit=crop',
        'taxes': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1200&h=600&fit=crop',
        'gaming': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1200&h=600&fit=crop'
    },
    
    // Generic/category images
    categories: {
        finance: 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&h=300&fit=crop',
        credit: 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400&h=300&fit=crop',
        money: 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400&h=300&fit=crop',
        business: 'https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=400&h=300&fit=crop'
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SiteImages;
}
